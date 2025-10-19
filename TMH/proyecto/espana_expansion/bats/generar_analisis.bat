@echo off
REM Script para generar análisis comparativos de todas las pruebas

echo.
echo ============================================================================
echo GENERANDO ANALISIS COMPARATIVOS
echo ============================================================================
echo.

REM Crear directorio de análisis
if not exist analisis_comparativos mkdir analisis_comparativos

echo Generando análisis de diferentes configuraciones...
echo.

REM Análisis de Mutación
if exist resultados_mutacion (
    echo [1/5] Analizando configuraciones de MUTACION...
    python comparar_resultados.py --directorio resultados_mutacion --nombre Mutacion --output-dir analisis_comparativos
    echo.
)

REM Análisis de Cruce
if exist resultados_cruce (
    echo [2/5] Analizando configuraciones de CRUCE...
    python comparar_resultados.py --directorio resultados_cruce --nombre Cruce --output-dir analisis_comparativos
    echo.
)

REM Análisis de Combinaciones
if exist resultados_combinaciones (
    echo [3/5] Analizando COMBINACIONES...
    python comparar_resultados.py --directorio resultados_combinaciones --nombre Combinaciones --output-dir analisis_comparativos
    echo.
)

REM Análisis de Elitismo
if exist resultados_elitismo (
    echo [4/5] Analizando configuraciones de ELITISMO...
    python comparar_resultados.py --directorio resultados_elitismo --nombre Elitismo --output-dir analisis_comparativos
    echo.
)

REM Análisis de Comparativa SA vs AG
if exist resultados_comparativa (
    echo [5/5] Analizando SA vs AG Elitismo 10%%...
    python comparar_resultados.py --directorio resultados_comparativa --nombre SA_vs_AG --output-dir analisis_comparativos
    echo.
)

echo.
echo ============================================================================
echo ANALISIS COMPLETADOS
echo ============================================================================
echo Todos los analisis se han guardado en: analisis_comparativos/
echo.
echo Archivos generados:
echo - Graficas de convergencia (.png)
echo - Graficas de metricas (.png)
echo - Rankings en JSON (.json)
echo ============================================================================
pause
