@echo off
REM Script para lanzar configuración 3 en una terminal separada
REM Ejecuta durante 8 horas con población grande

title AG - Config 3: Grande 8h

echo ============================================================================
echo CONFIGURACION 3: Poblacion Grande - 8 horas
echo ============================================================================
echo.
echo Iniciando...
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Pob_3000" --poblacion 3000 --guardar-json --guardar-grafica --output-dir resultados_8h

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
pause
