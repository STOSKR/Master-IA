# Memoria del Trabajo - Sistema ASR con Whisper

## Autores
[Completar con nombres de los autores]

## Resumen de Tareas Implementadas

### Tarea 1: Entrenamiento de ASR Monolingüe

#### 1.1 Tokenizador (`tarea1_1_tokenizador.ipynb`)
- **Objetivo**: Crear tokenizadores word-level para vocabulario fechas2
- **Implementación**: 
  - `Fechas2Tokenizer`: Tokenizador base con tokens especiales (<sos>, <eos>, <pad>)
  - `Fechas2BilingualTokenizer`: Combina vocabularios ES y EN
  - Guardado en formato pickle para reutilización
- **Resultado**: Vocabulario de ~150 palabras para español, ~200 para inglés

#### 1.2 Dataset con Augmentation (`tarea1_2_dataset.ipynb`)
- **Objetivo**: Cargar audio con augmentation realista
- **Implementación**:
  - `AdditiveNoise`: Ruido MUSAN con SNR 5-15 dB
  - `ReverbAugmentation`: Reverberación con RIR (largeroom)
  - `Fechas2Dataset`: Dataset con transformaciones aplicadas
- **Resultado**: Augmentation probabilístico (30% cada uno)

#### 1.3 Entrenamiento Español (`tarea1_3_entrenamiento_es.ipynb`)
- **Objetivo**: Transformer encoder-decoder para ASR español
- **Arquitectura**:
  - Frontend: 80 mel-spectrograms, log-compression, SpecAugment
  - Encoder: 6 capas, 256 d_model, 8 heads, self-attention
  - Decoder: 6 capas, causal attention + cross-attention
  - Salida: Generación autoregresiva con teacher forcing
- **Entrenamiento**: Adam 3e-4, 10 epochs, batch 16
- **Evaluación**: WER con jiwer, visualización attention maps

#### 1.4 Entrenamiento Inglés (`tarea1_4_entrenamiento_en.ipynb`)
- **Objetivo**: Misma arquitectura para inglés
- **Diferencias**: Solo cambia tokenizador y CSV de datos
- **Resultado**: Modelo independiente para inglés

### Tarea 2: Sistema Multitarea con Instrucciones

#### 2.1 Tokenizador con Instrucciones (`tarea2_multitarea.ipynb`)
- **Objetivo**: Tokenizador con 4 tipos de instrucciones
- **Implementación**:
  - Tokens de instrucción: `<transcribe_es>`, `<transcribe_en>`, `<translate_en_es>`, `<translate_es_en>`
  - Prefijo de secuencia indica tarea
- **Resultado**: Vocabulario bilingüe + 4 tokens especiales

#### 2.2 Dataset Multitarea
- **Objetivo**: Generar 4 ejemplos por cada par (audio, texto)
- **Implementación**:
  - Transcripción ES: audio español → texto español
  - Transcripción EN: audio inglés → texto inglés
  - Traducción EN→ES: audio inglés → texto español
  - Traducción ES→EN: audio español → texto inglés
- **Resultado**: 40k ejemplos de entrenamiento (10k×4)

#### 2.3 Evaluación por Tipo de Tarea
- **Objetivo**: Medir WER separado por acción
- **Implementación**: Filtrar test set por columna 'action', calcular WER individual
- **Resultado**: Permite identificar qué tareas son más difíciles

### Tarea 3: Function Calling (`tarea3_function_calling.ipynb`)

#### 3.1 Sistema con Llamadas a Funciones
- **Objetivo**: Generar código Python ejecutable desde audio
- **Funciones implementadas**:
  ```python
  relative_day(days_to_add, current_date='21/11/2025')
  next_day(day_name, current_date='21/11/2025')
  ```
- **Tokenizador**: Vocabulario extendido con tokens de código: `|`, `(`, `)`, `'`, `,`, `+`, `-`
- **Formato**: `"texto descriptivo | función(args)"`
- **Evaluación**:
  1. Generar texto con modelo
  2. Extraer función después de `|`
  3. Ejecutar con `eval()` en entorno seguro
  4. Comparar fecha resultante con referencia
  5. Calcular accuracy (% fechas correctas)

## Arquitectura del Transformer

### Frontend de Audio
- **Mel-spectrograms**: 80 bandas, ventana 25ms, hop 10ms
- **Log-compression**: Estabiliza magnitudes
- **SpecAugment**: Frequency masking (15 bins) + Time masking (35 frames)

### Encoder
- 6 capas transformer
- Self-attention multi-head (8 heads, 32 d_head)
- Feed-forward 512 dimensiones
- Layer normalization + residual connections

### Decoder
- 6 capas transformer
- Causal self-attention (no ve futuro)
- Cross-attention a salida del encoder
- Feed-forward 512 dimensiones
- Embedding de tokens + posicional

### Generación
- Autoregresiva con greedy decoding
- Empieza con `<sos>`, termina con `<eos>`
- Max length 30 tokens

## Resultados Esperados

### Métricas
- **WER (Word Error Rate)**: Métrica estándar ASR
- **Accuracy (Task 3)**: % de fechas correctamente calculadas

### Análisis
- Visualización de attention maps (encoder y cross-attention)
- Curvas de loss durante entrenamiento
- Análisis de errores por tipo de expresión

## Archivos Generados

```
trabajo/
├── tarea1_1_tokenizador.ipynb
├── tarea1_2_dataset.ipynb
├── tarea1_3_entrenamiento_es.ipynb
├── tarea1_4_entrenamiento_en.ipynb
├── tarea2_multitarea.ipynb
├── tarea3_function_calling.ipynb
├── fechas2_tokenizer_es.pkl
├── fechas2_tokenizer_en.pkl
├── fechas2_tokenizer_bilingual.pkl
├── fechas2_tokenizer_instruct.pkl
├── fechas2_tokenizer_function.pkl
├── model_fechas2_es.pt
├── model_fechas2_en.pt
├── model_fechas2_multitask.pt
├── model_fechas2_function.pt
└── memoria.md
```

## Conclusiones

1. **Tokenización word-level**: Suficiente para dominio limitado (fechas)
2. **Augmentation**: MUSAN + RIR mejoran robustez del modelo
3. **Multitask learning**: Sharing encoder permite transferencia entre idiomas
4. **Function calling**: Formato `texto | código` permite ejecutar acciones

## Referencias

- Vaswani et al. (2017): Attention Is All You Need
- Radford et al. (2023): Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)
- Dataset fechas2: Expresiones temporales en español e inglés
