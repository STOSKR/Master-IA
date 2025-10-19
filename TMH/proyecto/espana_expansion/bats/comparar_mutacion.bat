@echo off
REM Script para probar diferentes configuraciones de MUTACION

echo.
echo ============================================================================
echo PRUEBAS DE CONFIGURACIONES DE MUTACION
echo ============================================================================
echo.

REM Crear directorio de resultados
if not exist resultados_mutacion mkdir resultados_mutacion

echo Lanzando terminales para diferentes tasas de mutacion...
echo.

REM Mutación Baja (15%)
start "Mutacion 15%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut_15 --prob-mutacion 0.15 --prob-cruce 0.8 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_mutacion && echo. && echo COMPLETADO && pause"
REM Mutación Media-Baja (25%)
start "Mutacion 25%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut_25 --prob-mutacion 0.25 --prob-cruce 0.8 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_mutacion && echo. && echo COMPLETADO && pause"

timeout /t 5400 /nobreak > nul

REM Mutación Media (35%) - DEFAULT
start "Mutacion 35%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut_35 --prob-mutacion 0.35 --prob-cruce 0.8 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_mutacion && echo. && echo COMPLETADO && pause"
REM Mutación Media-Alta (50%)
start "Mutacion 50%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut_50 --prob-mutacion 0.50 --prob-cruce 0.8 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_mutacion && echo. && echo COMPLETADO && pause"

timeout /t 5400 /nobreak > nul

REM Mutación Alta (70%)
start "Mutacion 70%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut_70 --prob-mutacion 0.70 --prob-cruce 0.8 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_mutacion && echo. && echo COMPLETADO && pause"
REM Mutación Alta (90%)
start "Mutacion 90%%" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut_90 --prob-mutacion 0.90 --prob-cruce 0.8 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_mutacion && echo. && echo COMPLETADO && pause"

echo.
echo ============================================================================
echo TERMINALES LANZADOS - PRUEBAS DE MUTACION
echo ============================================================================
echo - Mutacion 15%% (1.5h)
echo - Mutacion 25%% (1.5h)
echo - Mutacion 35%% (1.5h) - BASELINE
echo - Mutacion 50%% (1.5h)
echo - Mutacion 70%% (1.5h) 
echo - Mutacion 90%% (1.5h)
echo.
echo Los resultados se guardaran en: resultados_mutacion/
echo ===================================================================
pause
