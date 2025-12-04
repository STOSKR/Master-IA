#!/bin/bash

#SBATCH -p long
#SBATCH --cpus-per-task=8
#SBATCH --job-name=transformer_decoder
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH -o logs/run11_transformer_%j.log

# Initialize conda for bash shell
source /opt/miniconda3/etc/profile.d/conda.sh

# Activate conda environment
conda activate RFA2526pt

# Install required packages if not already installed
pip install nbformat nbconvert ipykernel torch

python run_notebook_execution.py
