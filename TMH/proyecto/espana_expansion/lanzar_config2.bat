@echo off
REM Script para lanzar configuración 2 en una terminal separada
REM Ejecuta durante 8 horas con población mediana

title AG - Config 2: Mediana 8h

echo ============================================================================
echo CONFIGURACION 2: Poblacion Mediana - 8 horas
echo ============================================================================
echo.
echo Iniciando...
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Poblacion_1500_8h" --poblacion 1500 --guardar-json --guardar-grafica --output-dir resultados_8h

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
pause
