# Ejecutar Notebook en el Cluster

## Configuración del entorno

El script usa el entorno conda `base` por defecto. Si necesitas usar otro entorno:

```bash
# En run_notebook.sh, cambia esta línea:
conda activate base
# por:
conda activate nombre_de_tu_entorno
```

## Opción 1: Usando SLURM (Recomendado para cluster)

### Paso 1: Verificar dependencias

```bash
# Verificar que nbformat y nbconvert están instalados
pip list | grep nb

# Si no están, instalarlos:
./install_deps.sh
```

### Paso 2: Lanzar el trabajo

```bash
cd /home/alumno.upv.es/scheng1/W/Master-IA/2RNA
sbatch run_notebook.sh
```

### Paso 3: Monitorear el progreso

```bash
# Ver estado del job
squeue -u $USER

# Ver los logs en tiempo real
tail -f logs/mnist_high_acc_*.out
```

## Opción 2: Ejecución directa (para testing)

```bash
python run_notebook_execution.py
```

## Configuración actual del cluster

**Particiones disponibles:**
- `test` - Partición por defecto para pruebas
- `docencia` - **Configurada en el script** (para trabajos de docencia)
- `long` - Para trabajos largos

**Recursos asignados:**
- CPUs: 4
- RAM: 16GB
- GPU: 1x L40S
- Tiempo máximo: 2 horas
- Workers: Detecta automáticamente SLURM_CPUS_PER_TASK

## Outputs

- **Notebook ejecutado**: `mnist_high_accuracy_output_YYYYMMDD_HHMMSS.ipynb`
- **Logs SLURM**: `logs/mnist_high_acc_JOBID.out` y `.err`
- **Modelo entrenado**: `best_model_high_acc.pt`

## Cancelar un trabajo

```bash
scancel JOBID
```

## Ver trabajos anteriores

```bash
sacct -u $USER --format=JobID,JobName,State,Elapsed,MaxRSS
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'torch'"

El script ahora activa conda automáticamente. Si sigue fallando:

1. Verifica qué entorno conda tiene PyTorch:
```bash
conda env list
conda activate nombre_entorno
python -c "import torch; print(torch.__version__)"
```

2. Edita `run_notebook.sh` y cambia:
```bash
conda activate base
```
por el nombre de tu entorno correcto.

### Error: "invalid partition specified"

Las particiones válidas son: `test`, `docencia`, `long`

Edita `run_notebook.sh` línea 10:
```bash
#SBATCH --partition=docencia  # Cambiar si necesario
```
