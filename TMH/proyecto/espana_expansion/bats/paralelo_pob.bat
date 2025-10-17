@echo off
REM Script maestro para lanzar TODAS las configuraciones por pares

REM Crear directorio de resultados
if not exist resultados_poblacion mkdir resultados_poblacion

echo.
echo Lanzando primer par de terminales...
echo.

start "AG pob100 - Par 1" /wait cmd /c lanzar_pob100.bat
start "AG pob500 - Par 1" /wait cmd /c lanzar_pob500.bat

echo.
echo Primer par completado. Lanzando segundo par...
echo.

REM --- Par 2 ---
start "AG pob750 - Par 2" /wait cmd /c lanzar_pob750.bat
start "AG pob1000 - Par 2" /wait cmd /c lanzar_pob1000.bat

echo.
echo Segundo par completado. Lanzando tercer par...
echo.

REM --- Par 3 ---
start "AG pob3000 - Par 3" /wait cmd /c lanzar_pob3000.bat
start "AG pob5000 - Par 3" /wait cmd /c lanzar_pob5000.bat

echo.
echo ============================================================================
echo TODOS LOS PROCESOS COMPLETADOS
echo ============================================================================
pause