import pandas as pd
import numpy as np

df = pd.read_csv('Clean_Dataset.csv')

print('=== RELACIÓN: days_left vs price ===')
for days in [1, 7, 14, 21, 30, 45, 49]:
    subset = df[df['days_left'] == days]
    print(f'\n{days} días antes del vuelo:')
    print(f'  Número de registros: {len(subset)}')
    print(f'  Precio promedio: Rs.{subset["price"].mean():.2f}')
    print(f'  Precio mediano: Rs.{subset["price"].median():.2f}')
    print(f'  Min: Rs.{subset["price"].min():.0f} | Max: Rs.{subset["price"].max():.0f}')

print('\n\n=== ANÁLISIS DE TENDENCIA ===')
# Agrupar por días restantes y calcular promedio de precios
trend = df.groupby('days_left')['price'].agg(['mean', 'median', 'count']).reset_index()
trend = trend.sort_values('days_left')

print('\nCorrelación entre days_left y price:')
correlation = df['days_left'].corr(df['price'])
print(f'Correlación de Pearson: {correlation:.4f}')

print('\n=== EJEMPLO: ¿Cuándo comprar? ===')
print('Rangos de días y precios promedio:')
df['days_range'] = pd.cut(df['days_left'], bins=[0, 7, 14, 21, 35, 50], 
                           labels=['1-7 días', '8-14 días', '15-21 días', '22-35 días', '36-49 días'])
range_analysis = df.groupby('days_range')['price'].agg(['mean', 'median', 'count'])
print(range_analysis)
