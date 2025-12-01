#!/bin/bash

#SBATCH -p long
#SBATCH --cpus-per-task=8
#SBATCH --job-name=RNA_2_adamw
#SBATCH --mem=8G
#SBATCH -o logs/salida_%j.log # log de salida

# Initialize conda for bash shell
source /opt/miniconda3/etc/profile.d/conda.sh

# Activate conda environment
conda activate RFA2526pt

# Install required packages if not already installed
pip install nbformat nbconvert ipykernel

python run_notebook_execution.py