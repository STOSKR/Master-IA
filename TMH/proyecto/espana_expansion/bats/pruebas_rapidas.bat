@echo off
REM Script para PRUEBAS RAPIDAS (15 min) - Validación de configuraciones

echo.
echo ============================================================================
echo PRUEBAS RAPIDAS - Validacion de Configuraciones (15 min c/u)
echo ============================================================================
echo.

REM Crear directorio de resultados
if not exist pruebas_rapidas mkdir pruebas_rapidas

echo Lanzando pruebas rapidas para validacion...
echo.

REM Prueba 1: Mutación Baja
start "Test Mut15" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Test_Mut15 --prob-mutacion 0.15 --prob-cruce 0.8 --horas 0.25 --guardar-json --guardar-grafica --output-dir pruebas_rapidas && echo. && pause"

timeout /t 2 > nul

REM Prueba 2: Mutación Alta
start "Test Mut70" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Test_Mut70 --prob-mutacion 0.70 --prob-cruce 0.8 --horas 0.25 --guardar-json --guardar-grafica --output-dir pruebas_rapidas && echo. && pause"

timeout /t 2 > nul

REM Prueba 3: Cruce Bajo
start "Test Cruce50" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Test_Cruce50 --prob-mutacion 0.35 --prob-cruce 0.50 --horas 0.25 --guardar-json --guardar-grafica --output-dir pruebas_rapidas && echo. && pause"

timeout /t 2 > nul

REM Prueba 4: Baseline
start "Test Baseline" cmd /k "cd .. && python ejecutar_config_mutacion_cruce.py --nombre Test_Baseline --prob-mutacion 0.35 --prob-cruce 0.80 --horas 0.25 --guardar-json --guardar-grafica --output-dir pruebas_rapidas && echo. && pause"

echo.
echo ============================================================================
echo PRUEBAS RAPIDAS LANZADAS
echo ============================================================================
echo - Test Mut 15%% (15 min)
echo - Test Mut 70%% (15 min)
echo - Test Cruce 50%% (15 min)
echo - Test Baseline (15 min)
echo.
echo Tiempo total estimado: 15 minutos
echo.
echo Los resultados se guardaran en: pruebas_rapidas/
echo.
echo Una vez terminadas, ejecuta:
echo   python comparar_resultados.py --directorio pruebas_rapidas --nombre PruebasRapidas
echo ============================================================================
pause
