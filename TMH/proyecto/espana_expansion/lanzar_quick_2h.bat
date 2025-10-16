@echo off
REM Población 500, 2 horas - PRUEBA RAPIDA
title AG - Quick Test (2h)

echo ============================================================================
echo PRUEBA RAPIDA - Poblacion 500 - 2 horas
echo ============================================================================
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Quick_500_2h" --poblacion 500 --horas 2 --guardar-json --guardar-grafica --output-dir resultados_rapidos

echo.
echo COMPLETADO - Hora fin: %time%
pause
