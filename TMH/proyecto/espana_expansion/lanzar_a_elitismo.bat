@echo off
REM Lanzador maestro para comparativa de ELITISMO (5 configuraciones en paralelo)

if not exist resultados_elitismo mkdir resultados_elitismo

echo.
echo Lanzando terminales...
echo.

start "AG Elit 05" cmd /k lanzar_elitismo_05.bat
timeout /t 2 > nul

start "AG Elit 10" cmd /k lanzar_elitismo_10.bat
timeout /t 2 > nul

start "AG Elit 15" cmd /k lanzar_elitismo_15.bat
timeout /t 2 > nul

start "AG Elit 25" cmd /k lanzar_elitismo_25.bat
timeout /t 2 > nul

start "AG Elit 35" cmd /k lanzar_elitismo_35.bat

echo.
echo ============================================================================
echo 5 TERMINALES LANZADOS - Comparativa de Elitismo
echo ============================================================================
echo.
pause
