# Configuración del Token de HuggingFace

El notebook **P1_NLLB_RU-ZH.ipynb** requiere autenticación con HuggingFace para acceder a modelos privados o datasets.

## Opción 1: Variable de Entorno (Recomendado para Cluster)

1. Obtén tu token de HuggingFace:
   - Ve a https://huggingface.co/settings/tokens
   - Copia tu token de acceso (o crea uno nuevo con permisos de lectura)

2. Antes de ejecutar `sbatch`, exporta la variable:
   ```bash
   export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   sbatch run_P1.sh
   ```

3. Para que persista entre sesiones, añádelo a tu `~/.bashrc`:
   ```bash
   echo 'export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"' >> ~/.bashrc
   source ~/.bashrc
   ```

## Opción 2: Login Manual (Solo si ejecutas localmente)

Si ejecutas el notebook interactivamente (no con sbatch):
```bash
huggingface-cli login
```

Luego ingresa tu token cuando se solicite.

## Verificación

Para verificar que el token está configurado:
```bash
echo $HF_TOKEN
```

Debería mostrar tu token. Si está vacío, necesitas exportarlo de nuevo.

## Ejecución en el Cluster

```bash
# Opción A: Exportar y ejecutar
export HF_TOKEN="tu_token_aqui"
sbatch run_P1.sh

# Opción B: Inline (una sola línea)
HF_TOKEN="tu_token_aqui" sbatch run_P1.sh
```

## Notebooks que Requieren Token

- ✓ `P1_NLLB_RU-ZH.ipynb` - Requiere autenticación
- ✗ `P2_NLLB_Finetuning_RU-ZH.ipynb` - No requiere
- ✗ `P3_LLAMA_Finetuning_RU-ZH.ipynb` - No requiere  
- ✗ `P4_LLAMA_Prompting_RU-ZH.ipynb` - No requiere

## Troubleshooting

**Error:** `HF_TOKEN not found, proceeding without authentication`
- **Solución:** El token no está configurado. Usa `export HF_TOKEN="..."` antes de `sbatch`

**Error:** `Invalid token`
- **Solución:** Verifica que copiaste el token completo desde HuggingFace settings
