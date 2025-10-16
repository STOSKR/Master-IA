@echo off
REM Script para lanzar configuración 1 en una terminal separada
REM Ejecuta durante 8 horas con población pequeña

title AG - Config 1: Pequeña 8h

echo ============================================================================
echo CONFIGURACION 1: Poblacion Pequena - 8 horas
echo ============================================================================
echo.
echo Iniciando...
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Poblacion_500_8h" --poblacion 500 --elitismo 0.15 --horas 8 --guardar-json --guardar-grafica --dias 20 --lugares-por-dia 12 --output-dir resultados_8h

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
pause
