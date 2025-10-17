@echo off
title AG - Elitismo 25%

echo ============================================================================
echo Poblacion 1000 - Elitismo 25%%
echo ============================================================================
echo Hora inicio: %time%
echo.

cd ..
python ejecutar_config_individual.py --nombre "Elit_25" --elitismo 0.25  --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
