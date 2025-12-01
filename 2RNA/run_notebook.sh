#!/bin/bash

#SBATCH -p long
#SBATCH --cpus-per-task=8
#SBATCH --job-name=RNA_2_adamw
#SBATCH --mem=8G
#SBATCH -o logs/salida_%j.log # log de salida

conda activate RFA2526pt

python run_notebook_execution.py