#!/usr/bin/env python3
"""
Script para ejecutar el notebook run11_transformer_causal_decoder_text.ipynb y guardar los outputs.
Se puede ejecutar directamente o a través de SLURM.
"""

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from datetime import datetime
import os
import sys

def execute_notebook(notebook_path, output_path=None, timeout=7200):
    """
    Ejecuta un notebook de Jupyter y guarda los resultados.
    
    Args:
        notebook_path: Ruta al notebook a ejecutar
        output_path: Ruta donde guardar el notebook ejecutado (None = mismo nombre + _output)
        timeout: Timeout por celda en segundos (default: 2 horas)
    """
    print(f"Ejecutando notebook: {notebook_path}")
    print(f"Hora de inicio: {datetime.now()}")
    
    # Leer el notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Configurar el ejecutor
    ep = ExecutePreprocessor(
        timeout=timeout,
        kernel_name='python3',
        allow_errors=False  # Cambiar a True si quieres que continúe tras errores
    )
    
    try:
        # Ejecutar el notebook
        print("Comenzando ejecución...")
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path) or '.'}})
        
        # Determinar ruta de salida
        if output_path is None:
            base_name = os.path.splitext(notebook_path)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{base_name}_output_{timestamp}.ipynb"
        
        # Guardar el notebook ejecutado
        with open(output_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        
        print(f"\n✓ Ejecución completada exitosamente")
        print(f"✓ Outputs guardados en: {output_path}")
        print(f"Hora de finalización: {datetime.now()}")
        return True
        
    except Exception as e:
        print(f"\n✗ Error durante la ejecución:")
        print(f"  {type(e).__name__}: {e}")
        
        # Intentar guardar el notebook parcialmente ejecutado
        error_output = f"{os.path.splitext(notebook_path)[0]}_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ipynb"
        try:
            with open(error_output, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            print(f"✓ Notebook parcial guardado en: {error_output}")
        except:
            print("✗ No se pudo guardar el notebook parcial")
        
        return False

if __name__ == "__main__":
    # Configuración
    notebook_path = "run11_transformer_causal_decoder_text.ipynb"
    
    # Permitir pasar un notebook diferente como argumento
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    
    # Verificar que el notebook existe
    if not os.path.exists(notebook_path):
        print(f"Error: No se encontró el notebook '{notebook_path}'")
        sys.exit(1)
    
    # Ejecutar
    success = execute_notebook(notebook_path)
    
    # Salir con código apropiado
    sys.exit(0 if success else 1)
