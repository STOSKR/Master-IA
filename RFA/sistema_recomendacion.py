"""
SISTEMA DE RECOMENDACIÓN DE COMPRA DE VUELOS
Indica con probabilidades si conviene comprar ahora o esperar
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# ===== CARGA Y PREPROCESAMIENTO =====
print("🔄 Cargando y procesando datos...")
df = pd.read_csv('Clean_Dataset.csv')

# Preprocesamiento idéntico al notebook
df = df.drop(['Unnamed: 0', 'flight'], axis=1)
df['price_category'] = pd.qcut(df['price'], q=3, labels=['Bajo', 'Medio', 'Alto'])
df = df.drop('price', axis=1)
df = pd.get_dummies(df, columns=['airline', 'source_city', 'departure_time', 
                                  'stops', 'arrival_time', 'destination_city', 'class'], 
                    drop_first=True)

X = df.drop('price_category', axis=1)
y = df['price_category']

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, 
                                                      random_state=777, stratify=y)

# Estandarización
scaler = StandardScaler()
X_train['duration'] = scaler.fit_transform(X_train[['duration']])
X_test['duration'] = scaler.transform(X_test[['duration']])

# ===== ENTRENAMIENTO =====
print("🤖 Entrenando modelo Random Forest...")
modelo = RandomForestClassifier(random_state=777, n_estimators=100)
modelo.fit(X_train, y_train)

print("✅ Modelo entrenado exitosamente!\n")

# ===== FUNCIÓN DE RECOMENDACIÓN =====
def recomendar_compra(muestra_idx, X_test_original, modelo, scaler_obj):
    """
    Analiza una muestra y recomienda si comprar ahora o esperar
    """
    # Obtener el registro original
    registro = X_test_original.iloc[[muestra_idx]]
    days_left_actual = registro['days_left'].values[0]
    
    print("="*70)
    print(f"📋 ANÁLISIS DE VUELO #{muestra_idx}")
    print("="*70)
    print(f"⏰ Días hasta el vuelo: {int(days_left_actual)} días")
    
    # Predicción con probabilidades
    probabilidades = modelo.predict_proba(registro)[0]
    clase_predicha = modelo.classes_[np.argmax(probabilidades)]
    
    prob_bajo = probabilidades[0] * 100
    prob_medio = probabilidades[1] * 100
    prob_alto = probabilidades[2] * 100
    
    print(f"\n🎯 PREDICCIÓN ACTUAL ({int(days_left_actual)} días antes):")
    print(f"   Clase predicha: {clase_predicha}")
    print(f"   📊 Probabilidades:")
    print(f"      🟢 Precio BAJO:  {prob_bajo:.1f}%")
    print(f"      🟡 Precio MEDIO: {prob_medio:.1f}%")
    print(f"      🔴 Precio ALTO:  {prob_alto:.1f}%")
    
    # Simular escenario: ¿Qué pasaría si esperamos?
    if days_left_actual > 7:
        # Crear escenario futuro: 7 días antes del vuelo
        registro_futuro = registro.copy()
        registro_futuro['days_left'] = 7
        
        # Re-estandarizar duration si es necesario
        probabilidades_futuro = modelo.predict_proba(registro_futuro)[0]
        prob_bajo_futuro = probabilidades_futuro[0] * 100
        prob_medio_futuro = probabilidades_futuro[1] * 100
        prob_alto_futuro = probabilidades_futuro[2] * 100
        
        print(f"\n🔮 PREDICCIÓN FUTURA (si esperas a 7 días antes):")
        print(f"   📊 Probabilidades:")
        print(f"      🟢 Precio BAJO:  {prob_bajo_futuro:.1f}%")
        print(f"      🟡 Precio MEDIO: {prob_medio_futuro:.1f}%")
        print(f"      🔴 Precio ALTO:  {prob_alto_futuro:.1f}%")
        
        # Análisis de cambio
        cambio_alto = prob_alto_futuro - prob_alto
        cambio_bajo = prob_bajo_futuro - prob_bajo
        
        print(f"\n📈 CAMBIO ESPERADO:")
        print(f"   Probabilidad precio ALTO: {cambio_alto:+.1f}% puntos")
        print(f"   Probabilidad precio BAJO: {cambio_bajo:+.1f}% puntos")
        
        # RECOMENDACIÓN
        print(f"\n💡 RECOMENDACIÓN:")
        if cambio_alto > 10:
            print("   🔴 ¡COMPRA AHORA! El precio probablemente subirá")
            print(f"   → Riesgo de aumento: {cambio_alto:.1f}% puntos porcentuales")
        elif cambio_alto < -10:
            print("   🟢 ESPERA: El precio probablemente bajará")
            print(f"   → Oportunidad de ahorro: {abs(cambio_alto):.1f}% puntos porcentuales")
        else:
            print("   🟡 NEUTRAL: Cambio mínimo esperado")
            print(f"   → Variación pequeña: {abs(cambio_alto):.1f}% puntos porcentuales")
    else:
        print(f"\n⚠️  Ya estás cerca de la fecha (≤7 días)")
        print(f"   💡 RECOMENDACIÓN: Compra lo antes posible")
        print(f"   → Los precios tienden a subir cerca de la fecha")
    
    print("="*70)
    return {
        'days_left': days_left_actual,
        'prob_bajo': prob_bajo,
        'prob_medio': prob_medio,
        'prob_alto': prob_alto
    }

# ===== EJEMPLOS DE USO =====
print("\n" + "🎯 EJEMPLOS DE RECOMENDACIONES ".center(70, "=") + "\n")

# Analizar 3 casos diferentes
for i in [0, 100, 500]:
    recomendar_compra(i, X_test, modelo, scaler)
    print("\n")

# ===== ANÁLISIS ESTADÍSTICO GENERAL =====
print("\n" + "📊 ANÁLISIS ESTADÍSTICO GENERAL ".center(70, "="))
print("\nProbabilidad promedio de precio ALTO según días restantes:\n")

for days_range in [(1, 7), (8, 14), (15, 21), (22, 35), (36, 49)]:
    mask = (X_test['days_left'] >= days_range[0]) & (X_test['days_left'] <= days_range[1])
    subset = X_test[mask]
    
    if len(subset) > 0:
        probas = modelo.predict_proba(subset)
        prob_alto_promedio = probas[:, 2].mean() * 100  # Columna 2 = "Alto"
        print(f"   {days_range[0]:2d}-{days_range[1]:2d} días antes: "
              f"Prob. ALTO = {prob_alto_promedio:.1f}%")

print("\n" + "="*70)
print("✅ Análisis completado!")
print("\n💡 CONCLUSIÓN CLAVE:")
print("   → Reservar con 30+ días de antelación maximiza probabilidad de precio bajo")
print("   → Comprar con <7 días aumenta significativamente probabilidad de precio alto")
print("="*70)
