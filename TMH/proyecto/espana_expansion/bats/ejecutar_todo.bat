@echo off
REM Script MAESTRO para ejecutar todas las pruebas de configuración

echo.
echo ============================================================================
echo EXPERIMENTOS COMPLETOS - ALGORITMO GENETICO
echo ============================================================================
echo.
echo Este script lanzara TODAS las pruebas en paralelo:
echo - SA vs AG Elitismo 10%% (2 configuraciones)
echo - Configuraciones de Mutacion (5 configuraciones)
echo - Configuraciones de Cruce (5 configuraciones)
echo - Combinaciones Mutacion+Cruce (5 configuraciones)
echo.
echo TOTAL: 17 ejecuciones en paralelo
echo.
echo ADVERTENCIA: Esto consumira muchos recursos del sistema!
echo.
pause

REM Crear todos los directorios
if not exist resultados_comparativa mkdir resultados_comparativa
if not exist resultados_mutacion mkdir resultados_mutacion
if not exist resultados_cruce mkdir resultados_cruce
if not exist resultados_combinaciones mkdir resultados_combinaciones

echo.
echo ============================================================================
echo LANZANDO TODAS LAS PRUEBAS...
echo ============================================================================
echo.

REM Ejecutar todos los scripts de pruebas
echo Lanzando scripts de pruebas...
echo.

start "Control - SA vs Elit10" cmd /c comparar_sa_vs_elit10.bat
timeout /t 3 > nul

start "Control - Mutacion" cmd /c comparar_mutacion.bat
timeout /t 3 > nul

start "Control - Cruce" cmd /c comparar_cruce.bat
timeout /t 3 > nul

start "Control - Combinaciones" cmd /c comparar_combinaciones.bat
timeout /t 3 > nul

echo.
echo ============================================================================
echo TODAS LAS PRUEBAS LANZADAS
echo ============================================================================
echo.
echo Se han lanzado 17 terminales con diferentes configuraciones.
echo.
echo Una vez que TODAS las ejecuciones hayan terminado, ejecuta:
echo   generar_analisis.bat
echo.
echo Para generar las graficas comparativas y rankings.
echo ============================================================================
echo.
pause
