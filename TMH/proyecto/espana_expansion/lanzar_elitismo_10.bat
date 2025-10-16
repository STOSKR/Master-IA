@echo off
REM Población 1000, Elitismo 10%, 4 horas - EXPLORACION MODERADA
title AG - Elitismo 10% (4h)

echo ============================================================================
echo Poblacion 1000 - Elitismo 10%% - 4 horas - EXPLORACION MODERADA
echo ============================================================================
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Elit10_4h" --poblacion 1000 --elitismo 0.10  --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
