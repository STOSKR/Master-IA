@echo off
title AG - Elitismo 85%

echo ============================================================================
echo Poblacion 1000 - Elitismo 85%%
echo ============================================================================
echo Hora inicio: %time%
echo.

cd ..
python ejecutar_config_individual.py --nombre "Elit_35" --elitismo 0.85  --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
