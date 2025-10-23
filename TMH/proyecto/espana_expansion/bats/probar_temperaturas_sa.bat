@echo off
REM Script para probar diferentes temperaturas iniciales con Enfriamiento Simulado

echo.
echo ============================================================================
echo PRUEBA DE TEMPERATURAS INICIALES - ENFRIAMIENTO SIMULADO
echo ============================================================================
echo.
echo Este script ejecutara SA con diferentes temperaturas iniciales:
echo   - Temperatura 1
echo   - Temperatura 3
echo   - Temperatura 5
echo   - Temperatura 10
echo   - Temperatura 20
echo.
echo Cada ejecucion durara 4 horas
echo ============================================================================
echo.

REM Crear directorio de resultados
if not exist resultados_temperaturas mkdir resultados_temperaturas

echo Lanzando ejecuciones secuenciales...
echo.

REM Temperatura 1
echo [%time%] Lanzando SA con Temperatura = 1
start "SA Temp=1" cmd /k "cd .. && python enfriamiento_simulado.py 1 --horas 4 --temp 1 --guardar-json --guardar-grafica --output-dir resultados_temperaturas && echo. && echo COMPLETADO - Hora fin: %time% && pause"

timeout /t 60 > nul

REM Temperatura 3
echo [%time%] Lanzando SA con Temperatura = 3
start "SA Temp=3" cmd /k "cd .. && python enfriamiento_simulado.py 1 --horas 4 --temp 3 --guardar-json --guardar-grafica --output-dir resultados_temperaturas && echo. && echo COMPLETADO - Hora fin: %time% && pause"

echo Esperando 2 horas y 10 minutos antes de lanzar la siguiente...
timeout /t 7800 > nul

REM Temperatura 5
echo [%time%] Lanzando SA con Temperatura = 5
start "SA Temp=5" cmd /k "cd .. && python enfriamiento_simulado.py 1 --horas 4 --temp 5 --guardar-json --guardar-grafica --output-dir resultados_temperaturas && echo. && echo COMPLETADO - Hora fin: %time% && pause"

timeout /t 60 > nul

REM Temperatura 10
echo [%time%] Lanzando SA con Temperatura = 10
start "SA Temp=10" cmd /k "cd .. && python enfriamiento_simulado.py 1 --horas 4 --temp 10 --guardar-json --guardar-grafica --output-dir resultados_temperaturas && echo. && echo COMPLETADO - Hora fin: %time% && pause"

echo Esperando 2 horas y 10 minutos antes de lanzar la siguiente...
timeout /t 7800 > nul

REM Temperatura 20
echo [%time%] Lanzando SA con Temperatura = 20
start "SA Temp=20" cmd /k "cd .. && python enfriamiento_simulado.py 1 --horas 4 --temp 20 --guardar-json --guardar-grafica --output-dir resultados_temperaturas && echo. && echo COMPLETADO - Hora fin: %time% && pause"

timeout /t 60 > nul

REM Temperatura 100
echo [%time%] Lanzando SA con Temperatura = 100
start "SA Temp=100" cmd /k "cd .. && python enfriamiento_simulado.py 1 --horas 4 --temp 100 --guardar-json --guardar-grafica --output-dir resultados_temperaturas && echo. && echo COMPLETADO - Hora fin: %time% && pause"

echo Esperando 2 horas y 10 minutos antes de lanzar la siguiente...
timeout /t 7800 > nul

REM Temperatura 500
echo [%time%] Lanzando SA con Temperatura = 500
start "SA Temp=500" cmd /k "cd .. && python enfriamiento_simulado.py 1 --horas 4 --temp 500 --guardar-json --guardar-grafica --output-dir resultados_temperaturas && echo. && echo COMPLETADO - Hora fin: %time% && pause"

timeout /t 60 > nul

REM Temperatura 1000
echo [%time%] Lanzando SA con Temperatura = 1000
start "SA Temp=1000" cmd /k "cd .. && python enfriamiento_simulado.py 1 --horas 4 --temp 1000 --guardar-json --guardar-grafica --output-dir resultados_temperaturas && echo. && echo COMPLETADO - Hora fin: %time% && pause"


echo.
echo ============================================================================
echo TODAS LAS EJECUCIONES COMPLETADAS
echo ============================================================================
echo Se ejecutaron las siguientes configuraciones:
echo - SA con Temperatura inicial = 1
echo - SA con Temperatura inicial = 3
echo - SA con Temperatura inicial = 5
echo - SA con Temperatura inicial = 10
echo - SA con Temperatura inicial = 20
echo.
echo Duracion de cada ejecucion: 4 horas
echo Tiempo de espera entre ejecuciones: 2 horas y 10 minutos
echo Los resultados se guardaron en: resultados_temperaturas/
echo ============================================================================
pause
