@echo off
REM Lanzador maestro para comparativa de ELITISMO (5 configuraciones en paralelo)

echo ============================================================================
echo COMPARATIVA DE ELITISMO - 5 configuraciones en paralelo
echo ============================================================================
echo.
echo Se lanzaran 5 terminales:
echo   1. Elitismo  5%% - Alta exploracion
echo   2. Elitismo 10%% - Exploracion moderada
echo   3. Elitismo 15%% - Balanceado
echo   4. Elitismo 25%% - Explotacion moderada  
echo   5. Elitismo 35%% - Alta explotacion
echo.
echo Todas con poblacion 1000 durante 4 horas
echo Resultados en: resultados_elitismo/
echo.
echo ============================================================================
echo.

if not exist resultados_elitismo mkdir resultados_elitismo

echo Presione cualquier tecla para lanzar...
pause > nul

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
echo Cada terminal ejecutara 4 horas.
echo Puede cerrar esta ventana sin afectar las ejecuciones.
echo.
pause
