@echo off
REM Script para lanzar configuración 2 en una terminal separada
REM Ejecuta durante 8 horas con población mediana

title AG - Config 3

echo ============================================================================
echo CONFIGURACION 2: Poblacion Mediana - 8 horas
echo ============================================================================
echo.
echo Iniciando...
echo Hora inicio: %time%
echo.

python ejecutar_config_individual.py --nombre "Pob_1000" --poblacion 1000 --guardar-json --guardar-grafica --output-dir resultados_8h

echo.
echo ============================================================================
echo COMPLETADO
echo Hora fin: %time%
echo ============================================================================
echo.
