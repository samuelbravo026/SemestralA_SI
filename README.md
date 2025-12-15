# Spotify Popularity Analysis - Machine Learning

Interfaz web profesional para ejecutar y visualizar el análisis de Machine Learning del modelo `model_a.py` que predice la popularidad de canciones en Spotify.

## ⚡ INICIO RÁPIDO

**¿Primera vez? Lee [`INICIO_RAPIDO.md`](INICIO_RAPIDO.md) para empezar en 3 pasos.**

### Pasos esenciales:

1. **Inicia el servidor Flask:**
   - Windows: Ejecuta `start.bat`
   - Linux/Mac: Ejecuta `./start.sh`

2. **Abre `analisis.html` en tu navegador**

3. **Haz clic en "Ejecutar Análisis Completo"**

⚠️ **IMPORTANTE:** El servidor Flask DEBE estar corriendo antes de usar la interfaz.

## 🚀 Características

- **Ejecución del Modelo**: Ejecuta el pipeline completo de ML con un solo clic
- **Visualización de Métricas**: Muestra R², RMSE, MAE y más métricas clave
- **Galería de Imágenes**: Visualiza las 6 gráficas generadas por el modelo
- **Output en Tiempo Real**: Monitorea el progreso y output del análisis
- **Descarga de Reportes**: Genera y descarga reportes en formato texto
- **Diseño Responsive**: Funciona en desktop, tablet y móvil

## 📋 Estructura del Proyecto

```
SemestralA_SI/
├── model_a.py                    # Modelo de ML principal
├── app.py                        # Backend Flask API
├── requirements.txt              # Dependencias Python
├── index.html                    # Redirección a analisis.html
├── analisis.html                 # Interfaz web del modelo
├── css/
│   ├── styles.css               # Estilos generales
│   └── analisis.css             # Estilos específicos del análisis
├── js/
│   ├── main.js                  # JavaScript general
│   └── analisis.js              # JavaScript del análisis
└── INSTRUCCIONES_ANALISIS.md    # Documentación detallada
```

## 🛠️ Instalación

### 1. Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

### 2. Preparar el Dataset

Asegúrate de tener el archivo `universal_top_spotify_songs.csv` en el directorio raíz. Si no lo tienes, el modelo generará datos de ejemplo automáticamente.

## 🚀 Uso

### Paso 1: Iniciar el Servidor Flask

```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

### Paso 2: Abrir la Interfaz Web

Abre `index.html` en tu navegador o usa:

```bash
python -m http.server 8000
# Luego abre http://localhost:8000
```

### Paso 3: Ejecutar el Análisis

1. En la interfaz web, haz clic en **"Ejecutar Análisis Completo"**
2. Confirma la ejecución en el diálogo
3. Observa la barra de progreso mientras el modelo se ejecuta
4. Los resultados aparecerán automáticamente cuando termine

## 📊 Pipeline del Modelo

El modelo ejecuta las siguientes etapas:

### 4.1 Data Preparation
- Carga del dataset de Spotify
- Limpieza y validación de datos
- Creación de features

### 4.2 Exploratory Data Analysis
- Análisis univariado (distribución de popularidad)
- Análisis bivariado (explicit vs non-explicit)
- Matriz de correlaciones

### 5. Build Initial AI Model
- Entrenamiento de 4 modelos:
  - Linear Regression
  - Ridge Regression
  - Random Forest Regressor
  - Gradient Boosting Regressor

### 6. Develop Benchmark
- Comparación de modelos
- Selección del mejor modelo

### 7. Evaluate Primary Metrics
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score
- MAPE (Mean Absolute Percentage Error)

### 8. Evaluate Secondary Metrics
- Rendimiento computacional
- Uso de memoria
- Robustez ante ruido
- Métricas de equidad

## 📈 Visualizaciones Generadas

El modelo genera 6 visualizaciones:

1. **01_popularity_distribution.png**: Distribución de popularidad
2. **02_explicit_vs_popularity.png**: Comparación explicit vs non-explicit
3. **03_correlation_matrix.png**: Matriz de correlaciones
4. **04_feature_importance.png**: Importancia de features
5. **05_metrics_evaluation.png**: Evaluación de métricas
6. **06_predictions_analysis.png**: Análisis de predicciones

## 🔌 API Endpoints

### POST /api/run-analysis
Ejecuta el análisis completo del modelo

### GET /api/status
Obtiene el estado actual del análisis

### GET /api/results
Obtiene los resultados del último análisis

### GET /api/images/<image_name>
Sirve las imágenes generadas

### GET /api/dataset-info
Obtiene información del dataset

## 🛠️ Tecnologías Utilizadas

### Backend
- Python 3.8+
- Flask (Web framework)
- Pandas & NumPy (Data processing)
- Scikit-learn (Machine Learning)
- Matplotlib & Seaborn (Visualizations)

### Frontend
- HTML5
- CSS3 (Variables, Flexbox, Grid)
- JavaScript (ES6+)
- Font Awesome (Icons)

## 🔧 Troubleshooting

### Error: No se puede conectar al servidor API

**Solución:** Asegúrate de que Flask esté ejecutándose:
```bash
python app.py
```

### Error: ModuleNotFoundError

**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: FileNotFoundError - Dataset no encontrado

**Solución:** El modelo generará datos de ejemplo automáticamente. Si quieres usar datos reales, coloca `universal_top_spotify_songs.csv` en el directorio raíz.

## 📄 Licencia

Este proyecto es parte de un trabajo semestral académico.

---

**Desarrollado con ❤️ para análisis de Machine Learning en Spotify**
