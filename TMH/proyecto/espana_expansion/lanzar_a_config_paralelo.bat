@echo off
REM Script maestro para lanzar TODAS las configuraciones en terminales separadas

REM Crear directorio de resultados
if not exist resultados_8h mkdir resultados_8h

echo.
echo Lanzando terminales...
echo.

REM Lanzar cada configuración en una terminal nueva
start "AG Config 3" cmd /k lanzar_config3.bat
timeout /t 2 > nul

start "AG Config 4" cmd /k lanzar_config4.bat
timeout /t 2 > nul

start "AG Config 5" cmd /k lanzar_config5.bat
timeout /t 2 > nul

echo.
echo ============================================================================
echo TERMINALES LANZADOS
echo ============================================================================
