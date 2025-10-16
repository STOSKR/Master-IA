@echo off
REM Población 1000, Elitismo 25%, 4 horas - EXPLOTACION MODERADA
title AG - Elitismo 25% (4h)

echo ============================================================================
echo Poblacion 1000 - Elitismo 25%% - 4 horas - EXPLOTACION MODERADA
echo ============================================================================
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Elit25_4h" --poblacion 1000 --elitismo 0.25 --horas 4 --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
