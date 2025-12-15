#!/bin/bash

echo "================================================================================"
echo "SPOTIFY POPULARITY ANALYSIS - INICIANDO SERVIDOR"
echo "================================================================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python no está instalado"
    echo "Por favor instala Python 3.8+ desde https://www.python.org/"
    exit 1
fi

echo "[1/3] Verificando dependencias..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Instalando dependencias..."
    pip3 install -r requirements.txt
fi
echo "✓ Dependencias OK"

echo ""
echo "[2/3] Iniciando servidor Flask en http://localhost:5000"
echo ""
echo "IMPORTANTE: Deja esta terminal abierta mientras usas la interfaz"
echo "            Presiona Ctrl+C para detener el servidor"
echo ""
echo "================================================================================"
echo ""

# Iniciar Flask
python3 app.py
