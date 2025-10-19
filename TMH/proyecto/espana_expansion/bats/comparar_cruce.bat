@echo off
REM Script para probar diferentes configuraciones de CRUCE

echo.
echo ============================================================================
echo PRUEBAS DE CONFIGURACIONES DE CRUCE (CROSSOVER)
echo ============================================================================
echo.

REM Crear directorio de resultados
if not exist resultados_cruce mkdir resultados_cruce

echo Lanzando terminales para diferentes tasas de cruce...
echo.

REM Cruce Bajo (50%)
start "Cruce 50%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Cruce_50 --prob-mutacion 0.35 --prob-cruce 0.50 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_cruce && echo. && echo COMPLETADO && pause"

REM Cruce Medio-Bajo (65%)
start "Cruce 65%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Cruce_65 --prob-mutacion 0.35 --prob-cruce 0.65 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_cruce && echo. && echo COMPLETADO && pause"

timeout /t 15000 /nobreak > nul

REM Cruce Medio (80%) - DEFAULT
start "Cruce 80%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Cruce_80 --prob-mutacion 0.35 --prob-cruce 0.80 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_cruce && echo. && echo COMPLETADO && pause"
REM Cruce Alto (90%)
start "Cruce 90%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Cruce_90 --prob-mutacion 0.35 --prob-cruce 0.90 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_cruce && echo. && echo COMPLETADO && pause"

echo.
echo ============================================================================
echo TERMINALES LANZADOS - PRUEBAS DE CRUCE
echo ============================================================================
echo - Cruce 50%% (1.5h)
echo - Cruce 65%% (1.5h)
echo - Cruce 80%% (1.5h) - BASELINE
echo - Cruce 90%% (1.5h)
echo.
echo Los resultados se guardaran en: resultados_cruce/
echo ============================================================================
pause
