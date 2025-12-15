# 🚀 Inicio Rápido - Spotify Popularity Analysis

## ⚡ Pasos Simples para Empezar

### 1️⃣ Iniciar el Servidor (OBLIGATORIO)

**Windows:**
```bash
# Haz doble clic en:
start.bat

# O desde la terminal:
python app.py
```

**Linux/Mac:**
```bash
# Desde la terminal:
./start.sh

# O manualmente:
python3 app.py
```

**✅ Verifica que veas esto:**
```
SPOTIFY POPULARITY ANALYSIS API
API Running on http://localhost:5000
```

⚠️ **IMPORTANTE:** Deja esta ventana abierta mientras usas la interfaz.

---

### 2️⃣ Abrir la Interfaz Web

**Opción A - Abrir directamente (Recomendado):**
1. Abre tu navegador (Chrome, Firefox, Edge)
2. Arrastra el archivo `analisis.html` a la ventana del navegador
3. O navega a: `file:///C:/ruta/a/SemestralA_SI/analisis.html`

**Opción B - Usar servidor HTTP simple:**
```bash
# En otra terminal/ventana:
python -m http.server 8000

# Luego abre en el navegador:
http://localhost:8000/analisis.html
```

---

### 3️⃣ Ejecutar el Análisis

1. Haz clic en **"Ejecutar Análisis Completo"**
2. Confirma la ejecución
3. Espera ~30-60 segundos
4. ¡Los resultados aparecerán automáticamente!

---

## ❌ Solución de Problemas

### Error: "No se puede conectar al servidor API"

**Solución:**
1. Verifica que `app.py` esté corriendo (paso 1)
2. Verifica que veas en la terminal: `Running on http://localhost:5000`
3. Si no está corriendo, ejecuta `start.bat` (Windows) o `./start.sh` (Linux/Mac)

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución:**
```bash
pip install -r requirements.txt
```

### El análisis se queda cargando

**Solución:**
1. Revisa la terminal donde corre Flask para ver errores
2. Verifica que tengas espacio en disco
3. Intenta ejecutar directamente: `python model_a.py`

### La interfaz no carga los estilos

**Solución:**
Asegúrate de que estos archivos existan:
- `css/styles.css`
- `css/analisis.css`
- `js/main.js`
- `js/analisis.js`

---

## 📊 ¿Qué hace el modelo?

El análisis ejecuta un pipeline completo de Machine Learning:

1. **Data Preparation** - Carga y limpia los datos
2. **Exploratory Analysis** - Análisis estadístico
3. **Model Training** - Entrena 4 modelos de ML
4. **Benchmark** - Compara y selecciona el mejor
5. **Primary Metrics** - Calcula RMSE, MAE, R²
6. **Secondary Metrics** - Robustez, equidad, rendimiento

**Resultados generados:**
- 6 visualizaciones (gráficos PNG)
- Métricas de rendimiento
- Importancia de features
- Análisis completo

---

## 📁 Archivos Importantes

```
SemestralA_SI/
├── start.bat              ← EJECUTA ESTO (Windows)
├── start.sh               ← EJECUTA ESTO (Linux/Mac)
├── app.py                 ← Servidor Flask API
├── model_a.py             ← Modelo de Machine Learning
├── analisis.html          ← ABRE ESTO en el navegador
├── requirements.txt       ← Dependencias de Python
└── README.md              ← Documentación completa
```

---

## 💡 Consejos

- **Mantén la terminal abierta** mientras usas la interfaz
- **Primera ejecución** puede tardar un poco más (instala dependencias)
- **Dataset propio**: Coloca `universal_top_spotify_songs.csv` en la raíz
- **Modo oscuro**: Usa el botón de luna/sol en la interfaz

---

## 🆘 ¿Necesitas Ayuda?

1. Lee el `README.md` completo
2. Ejecuta `python test_backend.py` para probar el API
3. Revisa los logs en la terminal de Flask

---

**¡Listo para analizar! 🎵📊**
