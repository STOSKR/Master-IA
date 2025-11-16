@echo off
title AG - Elitismo 5%

echo ============================================================================
echo Poblacion 1000 - Elitismo 5%%
echo ============================================================================
echo Hora inicio: %time%
echo.

cd ..
python ejecutar_config_individual.py --nombre "Elit_05" --elitismo 0.05 --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
