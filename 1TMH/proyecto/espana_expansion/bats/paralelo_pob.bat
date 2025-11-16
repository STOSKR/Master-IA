@echo off

echo Lanzando Par 1 (pob100 y pob500)...
start "AG pob100" cmd /c lanzar_pob100.bat
start "AG pob500" cmd /c lanzar_pob500.bat

echo Esperando 4 horas 10 minutos...
REM Pausa de 15000 segundos (4 horas 10 minutos)
timeout /t 15000 /nobreak > nul

echo Lanzando Par 2 (pob750 y pob1000)...
start "AG pob750" cmd /c lanzar_pob750.bat
start "AG pob1000" cmd /c lanzar_pob1000.bat

echo Esperando 2 horas...
REM Pausa de 7800 segundos (2 horas 10 minutos)
timeout /t 15000 /nobreak > nul

echo Lanzando Par 3 (pob3000 y pob5000)...
start "AG pob3000" cmd /c lanzar_pob3000.bat
start "AG pob5000" cmd /c lanzar_pob5000.bat

echo Todos los procesos han sido lanzados.