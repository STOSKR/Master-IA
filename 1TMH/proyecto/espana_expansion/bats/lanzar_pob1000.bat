@echo off
REM Script para lanzar configuración 2 en una terminal separada
REM Ejecuta durante 8 horas con población mediana

title AG - Pob1000

echo Iniciando...
echo Hora inicio: %time%
echo.

cd ..
python ejecutar_config_individual.py --nombre "Pob_1000" --poblacion 1000 --guardar-json --guardar-grafica --output-dir resultados_poblacion

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
