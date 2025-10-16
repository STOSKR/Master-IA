@echo off
REM Población 2000, 12 horas - OVERNIGHT INTENSIVO
title AG - Intensivo (12h)

echo ============================================================================
echo OVERNIGHT INTENSIVO - Poblacion 2000 - 12 horas
echo ============================================================================
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Intensivo_2000_12h" --poblacion 2000 --elitismo 0.20 --horas 12 --guardar-json --guardar-grafica --output-dir resultados_12h

echo.
echo COMPLETADO - Hora fin: %time%
pause
