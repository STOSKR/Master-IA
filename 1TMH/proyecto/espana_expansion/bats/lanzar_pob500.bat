@echo off
REM Script para lanzar configuración 1 en una terminal separada
REM Ejecuta durante 8 horas con población pequeña

title AG - Pob500

echo Iniciando...
echo Hora inicio: %time%
echo.

cd ..
python ejecutar_config_individual.py --nombre "Pob_500" --poblacion 500 --guardar-json --guardar-grafica --output-dir resultados_poblacion

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
