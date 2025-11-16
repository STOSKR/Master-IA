@echo off
REM Script para probar combinaciones de MUTACION y CRUCE

echo.
echo ============================================================================
echo PRUEBAS DE COMBINACIONES MUTACION + CRUCE
echo ============================================================================
echo.

REM Crear directorio de resultados
if not exist resultados_combinaciones mkdir resultados_combinaciones

echo Lanzando terminales para diferentes combinaciones...
echo.

REM Combinación 1: Mutación Baja + Cruce Alto (Exploración conservadora)
start "Mut15_Cruce90" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut15_Cruce90 --prob-mutacion 0.15 --prob-cruce 0.90 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_combinaciones && echo. && echo COMPLETADO && pause"

timeout /t 2 > nul

REM Combinación 2: Mutación Media + Cruce Medio (Balance)
start "Mut35_Cruce80" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut35_Cruce80 --prob-mutacion 0.35 --prob-cruce 0.80 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_combinaciones && echo. && echo COMPLETADO && pause"

timeout /t 2 > nul

REM Combinación 3: Mutación Alta + Cruce Bajo (Exploración agresiva)
start "Mut70_Cruce50" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut70_Cruce50 --prob-mutacion 0.70 --prob-cruce 0.50 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_combinaciones && echo. && echo COMPLETADO && pause"

timeout /t 2 > nul

REM Combinación 4: Mutación Alta + Cruce Alto (Máxima exploración)
start "Mut60_Cruce90" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut60_Cruce90 --prob-mutacion 0.60 --prob-cruce 0.90 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_combinaciones && echo. && echo COMPLETADO && pause"

timeout /t 2 > nul

REM Combinación 5: Mutación Baja + Cruce Bajo (Convergencia rápida)
start "Mut20_Cruce60" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Mut20_Cruce60 --prob-mutacion 0.20 --prob-cruce 0.60 --horas 1.5 --guardar-json --guardar-grafica --output-dir resultados_combinaciones && echo. && echo COMPLETADO && pause"

echo.
echo ============================================================================
echo TERMINALES LANZADOS - PRUEBAS DE COMBINACIONES
echo ============================================================================
echo - Mut 15%% + Cruce 90%% (Exploración conservadora)
echo - Mut 35%% + Cruce 80%% (Balance - BASELINE)
echo - Mut 70%% + Cruce 50%% (Exploración agresiva)
echo - Mut 60%% + Cruce 90%% (Máxima exploración)
echo - Mut 20%% + Cruce 60%% (Convergencia rápida)
echo.
echo Los resultados se guardaran en: resultados_combinaciones/
echo ============================================================================
pause
