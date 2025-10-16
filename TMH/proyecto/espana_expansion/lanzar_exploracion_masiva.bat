@echo off
REM Población 5000, 8 horas - EXPLORACIÓN MASIVA
title AG - Exploración Masiva (8h)

echo ============================================================================
echo EXPLORACION MASIVA - Poblacion 5000 - Elitismo 10%% - 8 horas
echo ============================================================================
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Exploracion_5000_8h" --poblacion 5000 --elitismo 0.10 --guardar-json --guardar-grafica --output-dir resultados_8h

echo.
echo COMPLETADO - Hora fin: %time%
pause
