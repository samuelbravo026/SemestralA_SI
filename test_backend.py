#!/usr/bin/env python3
"""
Script de prueba para verificar que el backend Flask funciona correctamente
"""

import requests
import time

API_URL = "http://localhost:5000/api"

print("="*80)
print("PRUEBA DEL BACKEND FLASK API")
print("="*80)

# Paso 1: Verificar que el servidor está corriendo
print("\n1. Verificando servidor...")
try:
    response = requests.get("http://localhost:5000/")
    print(f"   ✓ Servidor responde: {response.status_code}")
    print(f"   Respuesta: {response.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("\n   Por favor, inicia el servidor con: python app.py")
    exit(1)

# Paso 2: Obtener estado inicial
print("\n2. Obteniendo estado inicial...")
try:
    response = requests.get(f"{API_URL}/status")
    print(f"   Estado: {response.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Paso 3: Obtener info del dataset
print("\n3. Obteniendo info del dataset...")
try:
    response = requests.get(f"{API_URL}/dataset-info")
    data = response.json()
    print(f"   Status: {data.get('status')}")
    if data.get('status') == 'success':
        print(f"   Registros: {data['info']['total_records']}")
        print(f"   Features: {data['info']['features']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Paso 4: Ejecutar análisis (comentado por defecto para no tardar)
print("\n4. Ejecutar análisis (comentado por defecto)")
print("   Para ejecutar el análisis, descomenta las líneas en test_backend.py")

# Descomenta esto para ejecutar el análisis:
# print("\n4. Ejecutando análisis...")
# try:
#     response = requests.post(f"{API_URL}/run-analysis")
#     data = response.json()
#     print(f"   Status: {data.get('status')}")
#     if data.get('status') == 'success':
#         print(f"   ✓ Análisis completado")
#         print(f"   Mejor modelo: {data['results']['metrics']['best_model']}")
#         print(f"   R² Score: {data['results']['metrics']['test_r2']:.4f}")
# except Exception as e:
#     print(f"   ✗ Error: {e}")

print("\n" + "="*80)
print("PRUEBA COMPLETADA")
print("="*80)
