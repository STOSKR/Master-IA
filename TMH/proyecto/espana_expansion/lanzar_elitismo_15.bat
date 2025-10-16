@echo off
REM Población 1000, Elitismo 15%, 4 horas - BALANCEADO (DEFAULT)
title AG - Elitismo 15% (4h)

echo ============================================================================
echo Poblacion 1000 - Elitismo 15%% - 4 horas - BALANCEADO
echo ============================================================================
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Elit15_4h" --poblacion 1000  --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
