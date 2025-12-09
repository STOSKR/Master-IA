#!/bin/bash

#SBATCH -p long
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --job-name=TLH_Tarea13
#SBATCH --mem=16G
#SBATCH -o logs/tarea13_%j.log

# Initialize conda for bash shell
source /opt/miniconda3/etc/profile.d/conda.sh

# Activate conda environment
conda activate RFA2526pt

# Install required packages if not already installed
pip install nbformat nbconvert ipykernel jiwer

# Set the kernel to use the conda environment
python -m ipykernel install --user --name RFA2526pt --display-name "RFA2526pt"

# Execute notebook (allow errors to save partial results)
jupyter nbconvert --to notebook --execute --allow-errors --ExecutePreprocessor.kernel_name=RFA2526pt Tarea1_3.ipynb --output Tarea1_3_output.ipynb
