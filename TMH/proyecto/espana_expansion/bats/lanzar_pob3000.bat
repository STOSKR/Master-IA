@echo off
REM Script para lanzar configuración 3 en una terminal separada
REM Ejecuta durante 8 horas con población grande

title AG - Pob3000

echo Iniciando...
echo Hora inicio: %time%
echo.

cd ..
python ejecutar_config_individual.py --nombre "Pob_3000" --poblacion 3000 --guardar-json --guardar-grafica --output-dir resultados_poblacion

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
