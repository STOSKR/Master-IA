@echo off
REM Script para comparar Enfriamiento Simulado vs AG con Elitismo 10%

echo.
echo ============================================================================
echo COMPARATIVA: Enfriamiento Simulado vs Algoritmo Genetico Elitismo 10%%
echo ============================================================================
echo.

REM Crear directorio de resultados
if not exist resultados_comparativa mkdir resultados_comparativa

echo Lanzando terminales...
echo.

REM Lanzar Enfriamiento Simulado
start "Enfriamiento Simulado" cmd /k "cd .. && python enfriamiento_simulado.py --horas 4 --guardar-json --guardar-grafica --output-dir resultados_comparativa && echo. && echo COMPLETADO - Hora fin: %time% && pause"

timeout /t 2 > nul

REM Lanzar AG con Elitismo 10%
start "AG Elitismo 10%%" cmd /k "cd .. && python ejecutar_config_individual.py --nombre SA_vs_Elit10 --elitismo 0.10 --horas 4 --guardar-json --guardar-grafica --output-dir resultados_comparativa && echo. && echo COMPLETADO - Hora fin: %time% && pause"

echo.
echo ============================================================================
echo TERMINALES LANZADOS
echo ============================================================================
echo - Enfriamiento Simulado (2 horas)
echo - AG Elitismo 10%% (2 horas)
echo.
echo Los resultados se guardaran en: resultados_comparativa/
echo ============================================================================
pause
