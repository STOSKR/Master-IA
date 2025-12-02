#!/bin/bash

#SBATCH -p long
#SBATCH --cpus-per-task=8
#SBATCH --job-name=P3
#SBATCH --mem=40G
#SBATCH --gres=gpu:1
#SBATCH -o logs/P3_%j.log

# Initialize conda
source /opt/miniconda3/etc/profile.d/conda.sh

# Activate conda environment
conda activate RFA2526pt

# Install required packages
pip install nbformat nbconvert ipykernel datasets evaluate transformers accelerate sacrebleu huggingface_hub peft bitsandbytes unbabel-comet

# Execute notebook
python << 'EOF'
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from datetime import datetime

notebook_path = "P3_LLAMA_Finetuning_RU-ZH.ipynb"
output_path = f"P3_LLAMA_Finetuning_RU-ZH_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ipynb"

print(f"Ejecutando notebook: {notebook_path}")
print(f"Hora de inicio: {datetime.now()}")

with open(notebook_path) as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=14400, kernel_name='python3')  # 4 horas timeout

try:
    print("Comenzando ejecución...")
    ep.preprocess(nb, {'metadata': {'path': './'}})
    print("✓ Ejecución completada exitosamente")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"✓ Notebook guardado en: {output_path}")
    
except Exception as e:
    print(f"✗ Error durante la ejecución:\n  {e}")
    error_path = f"P3_LLAMA_Finetuning_RU-ZH_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ipynb"
    with open(error_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"✓ Notebook parcial guardado en: {error_path}")
    raise

print(f"Hora de finalización: {datetime.now()}")
EOF
