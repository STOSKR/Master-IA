@echo off
REM Población 1000, Elitismo 5%, 4 horas - ALTA EXPLORACION
title AG - Elitismo 5% (4h)

echo ============================================================================
echo Poblacion 1000 - Elitismo 5%% - 4 horas - ALTA EXPLORACION
echo ============================================================================
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Elit05_4h" --poblacion 1000 --elitismo 0.05 --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
