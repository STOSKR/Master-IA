@echo off
title AG - Elitismo 10%

echo ============================================================================
echo Poblacion 1000 - Elitismo 10%%
echo ============================================================================
echo Hora inicio: %time%
echo.

cd ..
python ejecutar_config_individual.py --nombre "Elit_10" --elitismo 0.10  --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
