@echo off
REM Script para lanzar configuración 1 en una terminal separada
REM Ejecuta durante 8 horas con población pequeña

title AG - Pob100

echo Iniciando...
echo Hora inicio: %time%
echo.

cd ..
python ejecutar_config_individual.py --nombre "Pob_100" --poblacion 100 --guardar-json --guardar-grafica --output-dir resultados_poblacion

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
