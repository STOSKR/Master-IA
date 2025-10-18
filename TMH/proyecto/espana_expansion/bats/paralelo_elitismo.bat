@echo off
REM Lanzador maestro para comparativa de ELITISMO (pares en paralelo)

if not exist resultados_elitismo mkdir resultados_elitismo

echo.
echo Lanzando Par 1 (Elit 05 y Elit 10)...
echo.

REM --- Par 1 ---
set "TITLE1=AG Elit 05 - Par 1"
set "TITLE2=AG Elit 10 - Par 1"
start "%TITLE1%" cmd /c lanzar_elitismo_05.bat
start "%TITLE2%" cmd /c lanzar_elitismo_10.bat

:WaitLoop1
REM --- MODIFICADO ---
echo Esperando a que termine el Par 1 (revisando cada 2h 10min)...
REM Pausa larga
timeout /t 7800 /nobreak > nul
REM --- FIN MODIFICACIÓN ---
set PROC1_RUNNING=1
set PROC2_RUNNING=1
tasklist /fi "WINDOWTITLE eq %TITLE1%" 2>nul | find "cmd.exe" >nul && set PROC1_RUNNING=0
tasklist /fi "WINDOWTITLE eq %TITLE2%" 2>nul | find "cmd.exe" >nul && set PROC2_RUNNING=0
if %PROC1_RUNNING% == 0 goto WaitLoop1
if %PROC2_RUNNING% == 0 goto WaitLoop1
echo Par 1 completado.

echo.
echo Lanzando Par 2 (Elit 15 y Elit 25)...
echo.

REM --- Par 2 ---
set "TITLE3=AG Elit 15 - Par 2"
set "TITLE4=AG Elit 25 - Par 2"
start "%TITLE3%" cmd /c lanzar_elitismo_15.bat
start "%TITLE4%" cmd /c lanzar_elitismo_25.bat

:WaitLoop2
REM --- MODIFICADO ---
echo Esperando a que termine el Par 2 (revisando cada 2h 10min)...
REM Pausa larga
timeout /t 7800 /nobreak > nul
REM --- FIN MODIFICACIÓN ---
set PROC3_RUNNING=1
set PROC4_RUNNING=1
tasklist /fi "WINDOWTITLE eq %TITLE3%" 2>nul | find "cmd.exe" >nul && set PROC3_RUNNING=0
tasklist /fi "WINDOWTITLE eq %TITLE4%" 2>nul | find "cmd.exe" >nul && set PROC4_RUNNING=0
if %PROC3_RUNNING% == 0 goto WaitLoop2
if %PROC4_RUNNING% == 0 goto WaitLoop2
echo Par 2 completado.

echo.
echo Lanzando Par 3 (Elit 85 y Elit 95)...
echo.

REM --- Par 3 ---
set "TITLE5=AG Elit 85 - Par 3"
set "TITLE6=AG Elit 95 - Par 3"
start "%TITLE5%" cmd /c lanzar_elitismo_85.bat
start "%TITLE6%" cmd /c lanzar_elitismo_95.bat

:WaitLoop3
REM --- MODIFICADO ---
echo Esperando a que termine el Par 3 (revisando cada 2h 10min)...
REM Pausa larga
timeout /t 7800 /nobreak > nul
REM --- FIN MODIFICACIÓN ---
set PROC5_RUNNING=1
set PROC6_RUNNING=1
tasklist /fi "WINDOWTITLE eq %TITLE5%" 2>nul | find "cmd.exe" >nul && set PROC5_RUNNING=0
tasklist /fi "WINDOWTITLE eq %TITLE6%" 2>nul | find "cmd.exe" >nul && set PROC6_RUNNING=0
if %PROC5_RUNNING% == 0 goto WaitLoop3
if %PROC6_RUNNING% == 0 goto WaitLoop3
echo Par 3 completado.

echo.
echo ============================================================================
echo TODOS LOS PROCESOS COMPLETADOS
echo ============================================================================
echo.
pause