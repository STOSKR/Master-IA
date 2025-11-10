import json

# Cargar el notebook
with open('a:/Master-IA/RFA/entrega.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# IDs de celdas de subsecciones a actualizar
updates = {
    'f401f75b': {
        'find': '### 5.1 Modelos Lineales (T2)\n',
        'replace': '<a id="modelos-lineales"></a>\n### 5.1 Modelos Lineales (T2)\n'
    },
    'b30042a4': {
        'find': '### 5.2 Modelos Basados en Árboles (T5)\n',
        'replace': '<a id="modelos-arboles"></a>\n### 5.2 Modelos Basados en Árboles (T5)\n'
    },
    'fdc406fc': {
        'find': '### 5.3 Redes Neuronales Simples (T3)\n',
        'replace': '<a id="redes-simples"></a>\n### 5.3 Redes Neuronales Simples (T3)\n'
    },
    '3979c951': {
        'find': '### 5.4 Redes Neuronales Profundas (T4)\n',
        'replace': '<a id="redes-profundas"></a>\n### 5.4 Redes Neuronales Profundas (T4)\n'
    }
}

# Actualizar las celdas
for cell in nb['cells']:
    cell_id = cell.get('id', '')
    if cell_id in updates:
        update_info = updates[cell_id]
        # Buscar y reemplazar en la lista source
        for i, line in enumerate(cell['source']):
            if line == update_info['find']:
                cell['source'][i] = update_info['replace']
                print(f"✓ Anclaje añadido a celda {cell_id} para subsección {update_info['find'].strip()}")
                break

# Guardar el notebook actualizado
with open('a:/Master-IA/RFA/entrega.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("\n✓ Todos los anclajes de subsecciones han sido añadidos correctamente.")
