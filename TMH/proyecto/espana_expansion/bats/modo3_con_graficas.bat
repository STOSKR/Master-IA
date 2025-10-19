@echo off

REM Ejecutar el algoritmo genético con modo 3

echo EJECUTANDO MODO 3

cd ..
python algoritmo_espana.py 3

REM Verificar si la ejecución fue exitosa
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================================
    echo ERROR: El algoritmo genetico fallo con codigo de error %ERRORLEVEL%
    echo ============================================================================
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ============================================================================
echo ALGORITMO COMPLETADO - Iniciando generacion de graficas
echo ============================================================================
echo.

REM Ejecutar el análisis de gráficas

python analisis_graficas_espana.py ag_3.json

REM Verificar si el análisis fue exitoso
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================================
    echo ERROR: El analisis de graficas fallo con codigo de error %ERRORLEVEL%
    echo ============================================================================
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ============================================================================
echo PROCESO COMPLETADO EXITOSAMENTE
echo ============================================================================
echo.
echo Archivos generados:
echo   - ag_3.json (resultados del algoritmo)
echo   - Carpeta con graficas y analisis
echo.
echo ============================================================================
