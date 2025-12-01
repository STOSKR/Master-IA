#!/bin/bash
# Script para instalar las dependencias necesarias

echo "Instalando dependencias para ejecutar notebooks..."

pip install --user nbformat nbconvert jupyter

echo ""
echo "Dependencias instaladas. Ahora puedes:"
echo "1. Probar localmente: python run_notebook_execution.py"
echo "2. Lanzar al cluster: sbatch run_notebook.sh"
