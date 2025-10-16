@echo off
REM Población 1000, Elitismo 35%, 4 horas - ALTA EXPLOTACION
title AG - Elitismo 35% (4h)

echo ============================================================================
echo Poblacion 1000 - Elitismo 35%% - 4 horas - ALTA EXPLOTACION
echo ============================================================================
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Elit35_4h" --poblacion 1000 --elitismo 0.35  --guardar-json --guardar-grafica --output-dir resultados_elitismo

echo.
echo COMPLETADO - Hora fin: %time%
pause
