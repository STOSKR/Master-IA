@echo off
REM Script para lanzar configuración 1 en una terminal separada
REM Ejecuta durante 8 horas con población pequeña

title AG - Config 5
echo Iniciando...
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Pob_5000" --poblacion 5000 --guardar-json --guardar-grafica --output-dir resultados_8h

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
