#!/bin/bash
#SBATCH --job-name=mnist_high_acc
#SBATCH --partition=test
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --output=mnist_train_%j.log

# Cargar módulos si es necesario (ejemplo común, ajusta según tu cluster)
# module load cuda/11.8
# module load python/3.9

# Activar entorno virtual si tienes uno
# source venv/bin/activate

echo "Iniciando entrenamiento en el nodo: $SLURMD_NODENAME"
echo "CPUs asignadas: $SLURM_CPUS_PER_TASK"

python train_mnist.py
