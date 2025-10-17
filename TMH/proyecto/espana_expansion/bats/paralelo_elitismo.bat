@echo off
REM Lanzador maestro para comparativa de ELITISMO (5 configuraciones en paralelo)

if not exist resultados_elitismo mkdir resultados_elitismo

echo.
echo Lanzando primer par de terminales...
echo.

start "AG Elit 05 - Par 1" /wait cmd /c lanzar_elitismo_05.bat
start "AG Elit 10 - Par 1" /wait cmd /c lanzar_elitismo_10.bat

echo.
echo Primer par completado. Lanzando segundo par...
echo.

REM --- Par 2 ---
start "AG Elit 15 - Par 2" /wait cmd /c lanzar_elitismo_15.bat
start "AG Elit 25 - Par 2" /wait cmd /c lanzar_elitismo_25.bat

echo.
echo Segundo par completado. Lanzando tercer par...
echo.

REM --- Par 3 ---
start "AG Elit 35 - Par 3" /wait cmd /c lanzar_elitismo_85.bat
start "AG Elit 35 - Par 3" /wait cmd /c lanzar_elitismo_95.bat
echo.
echo ============================================================================
echo 5 TERMINALES LANZADOS - Comparativa de Elitismo
echo ============================================================================
echo.