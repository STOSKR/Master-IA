@echo off
REM Script para monitorear el progreso de todas las ejecuciones en tiempo real

title Monitor de Progreso - Experimentos AG

echo.
echo ============================================================================
echo MONITOR DE PROGRESO - Experimentos AG
echo ============================================================================
echo.
echo Este monitor mostrara en tiempo real:
echo - Numero de resultados completados por categoria
echo - Ultimo fitness alcanzado
echo - Mejores resultados por categoria
echo.
echo Se actualiza cada 30 segundos.
echo.
echo Presiona CTRL+C para salir
echo ============================================================================
echo.

cd ..
python monitor_progreso.py --intervalo 30

pause
