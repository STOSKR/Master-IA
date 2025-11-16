import json

# Cargar el notebook
with open('a:/Master-IA/RFA/entrega.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# IDs de celdas a actualizar con sus respectivos anclajes
updates = {
    '32930962': {
        'anchor': '<a id="metodologia"></a>\n',
        'starts_with': '## 4.'
    },
    'f401f75b': {
        'anchor': '<a id="implementacion"></a>\n',
        'starts_with': '## 5.'
    },
    'b0d877d5': {
        'anchor': '<a id="resultados"></a>\n',
        'starts_with': '## 6.'
    },
    'eb03f9a1': {
        'anchor': '<a id="conclusiones"></a>\n',
        'starts_with': '## 7.'
    },
    '698b2a31': {
        'anchor': '<a id="referencias"></a>\n',
        'starts_with': '## 8.'
    }
}

# Actualizar las celdas
for cell in nb['cells']:
    cell_id = cell.get('id', '')
    if cell_id in updates:
        update_info = updates[cell_id]
        # Verificar que la celda comience con el texto esperado
        if cell['source'] and cell['source'][0].startswith(update_info['starts_with']):
            # Insertar el anclaje al principio
            cell['source'].insert(0, update_info['anchor'])
            print(f"✓ Anclaje añadido a celda {cell_id} (Sección {update_info['starts_with']})")

# Guardar el notebook actualizado
with open('a:/Master-IA/RFA/entrega.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("\n✓ Todos los anclajes HTML han sido añadidos correctamente.")
