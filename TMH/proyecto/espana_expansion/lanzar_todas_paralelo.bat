@echo off
REM Script maestro para lanzar TODAS las configuraciones en terminales separadas

echo ============================================================================
echo LANZADOR DE CONFIGURACIONES EN PARALELO
echo ============================================================================
echo.
echo Este script abrira 3 terminales separados, cada uno ejecutando una
echo configuracion diferente durante 8 horas.
echo.
echo Configuraciones:
echo   1. Poblacion 500  - Terminal 1
echo   2. Poblacion 1500 - Terminal 2  
echo   3. Poblacion 3000 - Terminal 3
echo.
echo Cada terminal guardara sus resultados en: resultados_8h/
echo.
echo ============================================================================
echo.

REM Crear directorio de resultados
if not exist resultados_8h mkdir resultados_8h

echo Presione cualquier tecla para lanzar las 3 configuraciones...
pause > nul

echo.
echo Lanzando terminales...
echo.

REM Lanzar cada configuración en una terminal nueva
start "AG Config 1" cmd /k lanzar_config1.bat
timeout /t 2 > nul

start "AG Config 2" cmd /k lanzar_config2.bat
timeout /t 2 > nul

start "AG Config 3" cmd /k lanzar_config3.bat

echo.
echo ============================================================================
echo TERMINALES LANZADOS
echo ============================================================================
echo.
echo Se han abierto 3 terminales. Cada uno ejecutara su configuracion
echo de forma independiente durante 8 horas.
echo.
echo Puede cerrar esta ventana. Los otros procesos continuaran ejecutandose.
echo.
echo Para detener una ejecucion: Presione Ctrl+C en la terminal correspondiente
echo.
echo ============================================================================
echo.
pause
