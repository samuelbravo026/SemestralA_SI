@echo off
echo ================================================================================
echo SPOTIFY POPULARITY ANALYSIS - INICIANDO SERVIDOR
echo ================================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo Por favor instala Python 3.8+ desde https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)
echo ✓ Dependencias OK

echo.
echo [2/3] Iniciando servidor Flask en http://localhost:5000
echo.
echo IMPORTANTE: Deja esta ventana abierta mientras usas la interfaz
echo            Presiona Ctrl+C para detener el servidor
echo.
echo ================================================================================
echo.

REM Iniciar Flask
python app.py

pause
