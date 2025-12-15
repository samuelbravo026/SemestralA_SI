# 🔍 Guía de Debugging - Model_a.py no se ejecuta

Si al hacer clic en "Ejecutar Análisis Completo" no pasa nada o da error, sigue estos pasos:

## 1️⃣ Verificar que Flask esté corriendo

**En la terminal/CMD donde ejecutaste `start.bat` o `python app.py`, deberías ver:**

```
================================================================================
SPOTIFY POPULARITY ANALYSIS API
================================================================================

API Running on http://localhost:5000
```

✅ Si NO ves esto, Flask no está corriendo. Ejecuta `start.bat` o `python app.py`

---

## 2️⃣ Ver los logs del servidor

**Cuando hagas clic en el botón, la terminal de Flask debe mostrar:**

```
Starting analysis with Python: C:\...\python.exe
Current directory: C:\...\SemestralA_SI
Analysis completed with return code: 0
```

### ¿Qué significan los códigos?

- **Return code 0**: ✅ Éxito
- **Return code 1**: ❌ Error en model_a.py
- **ERROR: ...**: ❌ Ver el mensaje de error

---

## 3️⃣ Probar model_a.py directamente

En otra terminal/CMD:

```bash
cd C:\SemestralA_SI
python model_a.py
```

### Si funciona:
✅ El problema está en la comunicación Flask ↔ Navegador

### Si NO funciona:
❌ Verás el error específico. Puede ser:

**Error: No module named 'pandas'**
```bash
# Solución:
pip install -r requirements.txt
```

**Error: Permission denied**
```bash
# Solución: Ejecuta CMD/PowerShell como Administrador
```

---

## 4️⃣ Verificar consola del navegador

**Abre la consola de desarrollador:**
- Chrome/Edge: Presiona `F12` o `Ctrl+Shift+I`
- Firefox: Presiona `F12`

**Busca errores en la pestaña "Console":**

### Error común: "Failed to fetch"
```
Error: Failed to fetch http://localhost:5000/api/run-analysis
```
**Solución:** Flask no está corriendo. Ve al paso 1.

### Error común: "CORS policy"
```
Access to fetch at 'http://localhost:5000' blocked by CORS policy
```
**Solución:** Reinstala flask-cors:
```bash
pip install flask-cors
```

---

## 5️⃣ Probar el API manualmente

**Abre otra terminal y ejecuta:**

```bash
curl -X POST http://localhost:5000/api/run-analysis
```

### Respuesta exitosa:
```json
{
  "status": "success",
  "results": { ... }
}
```

### Respuesta con error:
```json
{
  "status": "error",
  "message": "...",
  "error": "...",
  "details": "..."
}
```

📋 **Copia el error completo y búscalo para entender qué falló.**

---

## 6️⃣ Revisar permisos de archivos

Verifica que tengas permisos de escritura en la carpeta:

```bash
# Windows (PowerShell):
(Get-Acl .).Access

# El usuario debe tener "FullControl" o "Modify"
```

El modelo necesita crear:
- `data_processed_clean.csv`
- `01_popularity_distribution.png`
- `02_explicit_vs_popularity.png`
- ... (6 imágenes PNG en total)

---

## 7️⃣ Verificar dependencias

```bash
python -c "import pandas, numpy, matplotlib, seaborn, sklearn, scipy, psutil, flask, flask_cors; print('✓ Todas las dependencias instaladas')"
```

Si falla, reinstala:
```bash
pip install -r requirements.txt
```

---

## 8️⃣ Modo Debug Avanzado

Edita `app.py` y cambia la última línea:

```python
# Antes:
app.run(debug=True, port=5000)

# Después (muestra más logs):
app.run(debug=True, port=5000, use_reloader=False)
```

Reinicia Flask y vuelve a intentar.

---

## 📝 Checklist Rápido

Marca los que ya verificaste:

- [ ] Flask está corriendo en http://localhost:5000
- [ ] La terminal de Flask muestra logs cuando hago clic en el botón
- [ ] `python model_a.py` funciona directamente
- [ ] La consola del navegador no muestra errores
- [ ] Tengo permisos de escritura en la carpeta
- [ ] Todas las dependencias están instaladas
- [ ] El puerto 5000 no está siendo usado por otro programa

---

## 🆘 Errores Comunes y Soluciones

### "ModuleNotFoundError: No module named 'X'"
```bash
pip install -r requirements.txt
```

### "Address already in use: Port 5000"
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

### "python: command not found"
```bash
# Prueba con:
python3 app.py
# O:
py app.py
```

### El análisis se queda "cargando" infinitamente
- Revisa la terminal de Flask para ver si hay errores
- El modelo puede tardar 30-60 segundos, es normal
- Si pasan más de 5 minutos, hay un timeout

---

## 💡 Información Útil

**Tiempo esperado de ejecución:** 30-60 segundos

**Archivos que debe generar:**
- 6 imágenes PNG (visualizaciones)
- 1 archivo CSV (datos procesados)

**Memoria requerida:** ~500 MB

**Python requerido:** 3.8 o superior

---

## 📞 Siguiente Paso

Si seguiste todos los pasos y aún no funciona:

1. Copia el error COMPLETO de la terminal de Flask
2. Copia el error de la consola del navegador
3. Ejecuta: `python --version` y copia la salida
4. Ejecuta: `pip list | findstr flask` y copia la salida

Con esa información podrás buscar la solución específica.
