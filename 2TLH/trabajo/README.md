# ASR con Transformer - Trabajo 2TLH

Sistema completo de reconocimiento automático de voz (ASR) con arquitectura Transformer encoder-decoder, basado en Whisper.

## Estructura del Proyecto

### Notebooks Implementados

1. **tarea1_1_tokenizador.ipynb**
   - Tokenizadores word-level para español, inglés y bilingüe
   - Guarda .pkl files para reutilización

2. **tarea1_2_dataset.ipynb**
   - Dataset con augmentation (MUSAN noise + RIR reverb)
   - Visualización de espectrogramas

3. **tarea1_3_entrenamiento_es.ipynb**
   - Transformer completo para ASR español
   - Arquitectura: 6 capas, 256 d_model, 8 heads
   - Evaluación con WER

4. **tarea1_4_entrenamiento_en.ipynb**
   - ASR inglés (reutiliza arquitectura)

5. **tarea2_multitarea.ipynb**
   - Sistema multitarea con instrucciones
   - 4 acciones: transcribe_es, transcribe_en, translate_en_es, translate_es_en
   - Evaluación separada por acción

6. **tarea3_function_calling.ipynb**
   - Generación de código Python ejecutable
   - Funciones: relative_day(), next_day()
   - Evaluación: accuracy de fechas calculadas

## Requisitos

```bash
pip install torch torchaudio pandas numpy scipy jiwer matplotlib ipython
```

### Datos Necesarios

- **fechas2/**: Dataset con audio y transcripciones
  - fechas2_train.es.csv / fechas2_test.es.csv
  - fechas2_train.en.csv / fechas2_test.en.csv
  - fechas2_test_instruct.csv
  - fechas2_train_function.es.csv / fechas2_train_function.en.csv
  - fechas2_test_function.csv

- **musan_small/**: Ruidos para augmentation
  - noise/free-sound/*.wav

- **RIRS_NOISES_small/**: Reverberaciones RIR
  - simulated_rirs/largeroom/*.wav

## Orden de Ejecución

### Tarea 1: ASR Monolingüe

```
1. tarea1_1_tokenizador.ipynb      → Genera tokenizers .pkl
2. tarea1_2_dataset.ipynb          → Valida augmentation
3. tarea1_3_entrenamiento_es.ipynb → Entrena modelo español
4. tarea1_4_entrenamiento_en.ipynb → Entrena modelo inglés
```

### Tarea 2: Multitarea

```
5. tarea2_multitarea.ipynb → Entrena y evalúa sistema con instrucciones
```

### Tarea 3: Function Calling

```
6. tarea3_function_calling.ipynb → Sistema con ejecución de código
```

## Arquitectura del Modelo

### Audio Frontend
- Mel-spectrograms: 80 bandas, 25ms ventana, 10ms hop
- Log-compression
- SpecAugment (freq_mask=15, time_mask=35)

### Encoder
- 6 capas Transformer
- Self-attention: 8 heads × 32 d_head
- Feed-forward: 512 dim
- Dropout: 0.1

### Decoder
- 6 capas Transformer
- Causal self-attention
- Cross-attention al encoder
- Feed-forward: 512 dim
- Generación autoregresiva

## Evaluación

### Métricas
- **WER (Word Error Rate)**: Tarea 1 y 2
- **Accuracy**: Tarea 3 (% fechas correctas)

### Visualizaciones
- Curvas de loss
- Attention maps (encoder y cross-attention)
- Espectrogramas con augmentation

## Resultados

Los modelos entrenados se guardan como:
- `model_fechas2_es.pt`
- `model_fechas2_en.pt`
- `model_fechas2_multitask.pt`
- `model_fechas2_function.pt`

Los tokenizadores se guardan como:
- `fechas2_tokenizer_es.pkl`
- `fechas2_tokenizer_en.pkl`
- `fechas2_tokenizer_bilingual.pkl`
- `fechas2_tokenizer_instruct.pkl`
- `fechas2_tokenizer_function.pkl`

## Notas de Implementación

### Tarea 3: Function Calling

El sistema genera texto con formato:
```
"descripción textual | función_python(args)"
```

Ejemplo:
```
"tomorrow | relative_day(+1)"
"next thursday | next_day('thursday')"
```

La evaluación extrae y ejecuta el código después de `|`, comparando la fecha resultante con la referencia.

## Autores

[Completar con nombres]

## Referencias

- Vaswani et al. (2017): Attention Is All You Need
- Radford et al. (2023): Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)
