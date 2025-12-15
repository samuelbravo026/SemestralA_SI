# Interfaz Web para Análisis de Popularidad de Spotify

## Descripción

Interfaz web profesional para ejecutar y visualizar el análisis de Machine Learning del modelo `model_a.py` que predice la popularidad de canciones en Spotify.

## Características

- **Ejecución del Modelo**: Ejecuta el pipeline completo de ML con un solo clic
- **Visualización de Métricas**: Muestra R², RMSE, MAE y más métricas clave
- **Galería de Imágenes**: Visualiza las 6 gráficas generadas por el modelo
- **Output en Tiempo Real**: Monitorea el progreso y output del análisis
- **Descarga de Reportes**: Genera y descarga reportes en formato texto
- **Diseño Responsive**: Funciona en desktop, tablet y móvil

## Instalación

### 1. Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- Flask (backend API)
- flask-cors (CORS support)
- pandas, numpy (procesamiento de datos)
- matplotlib, seaborn (visualizaciones)
- scikit-learn (modelos de ML)
- scipy, psutil (métricas adicionales)

### 2. Preparar el Dataset

Asegúrate de tener el archivo `universal_top_spotify_songs.csv` en el directorio raíz. Si no lo tienes, el modelo generará datos de ejemplo automáticamente.

## Uso

### Paso 1: Iniciar el Servidor Flask

```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

Deberías ver:
```
================================================================================
SPOTIFY POPULARITY ANALYSIS API
================================================================================

API Running on http://localhost:5000

Available endpoints:
  • POST /api/run-analysis - Run ML analysis
  • GET  /api/status - Get analysis status
  • GET  /api/results - Get analysis results
  • GET  /api/images/<name> - Get generated images
  • GET  /api/dataset-info - Get dataset information
================================================================================
```

### Paso 2: Abrir la Interfaz Web

Abre `analisis.html` en tu navegador. Puedes hacerlo de dos maneras:

**Opción A: Directamente desde el explorador**
- Navega a la carpeta del proyecto
- Abre `analisis.html` con doble clic

**Opción B: Usando un servidor web simple**
```bash
# Python 3
python -m http.server 8000

# Luego abre http://localhost:8000/analisis.html
```

### Paso 3: Ejecutar el Análisis

1. En la interfaz web, haz clic en **"Ejecutar Análisis Completo"**
2. Confirma la ejecución en el diálogo
3. Observa la barra de progreso mientras el modelo se ejecuta
4. Los resultados aparecerán automáticamente cuando termine

## Estructura de Archivos

```
SemestralA_SI/
├── model_a.py                    # Modelo de ML principal
├── app.py                        # Backend Flask API
├── requirements.txt              # Dependencias Python
├── analisis.html                 # Interfaz web del modelo
├── css/
│   ├── styles.css               # Estilos generales
│   └── analisis.css             # Estilos específicos del análisis
├── js/
│   ├── main.js                  # JavaScript general
│   └── analisis.js              # JavaScript del análisis
├── index.html                   # Dashboard principal
├── usuarios.html                # Gestión de usuarios
├── productos.html               # Gestión de productos
└── [imágenes generadas].png     # Visualizaciones del modelo
```

## Pipeline del Modelo

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

## Visualizaciones Generadas

El modelo genera 6 visualizaciones:

1. **01_popularity_distribution.png**: Distribución de popularidad
2. **02_explicit_vs_popularity.png**: Comparación explicit vs non-explicit
3. **03_correlation_matrix.png**: Matriz de correlaciones
4. **04_feature_importance.png**: Importancia de features
5. **05_metrics_evaluation.png**: Evaluación de métricas
6. **06_predictions_analysis.png**: Análisis de predicciones

## API Endpoints

### POST /api/run-analysis
Ejecuta el análisis completo del modelo

**Respuesta exitosa:**
```json
{
  "status": "success",
  "message": "Analysis completed successfully",
  "results": {
    "status": "completed",
    "timestamp": "2024-01-01T12:00:00",
    "metrics": {
      "best_model": "Random Forest",
      "test_r2": 0.8542,
      "test_rmse": 12.34,
      "test_mae": 8.76
    },
    "images": [...],
    "output": "..."
  }
}
```

### GET /api/status
Obtiene el estado actual del análisis

**Respuesta:**
```json
{
  "status": "idle|running|completed|error",
  "timestamp": "2024-01-01T12:00:00"
}
```

### GET /api/results
Obtiene los resultados del último análisis

### GET /api/images/<image_name>
Sirve las imágenes generadas

### GET /api/dataset-info
Obtiene información del dataset

## Características de la Interfaz

### Panel de Control
- Botón para ejecutar análisis
- Barra de progreso en tiempo real
- Información del dataset
- Estado del análisis

### Métricas Visuales
- Tarjetas con métricas clave
- Iconos y colores distintivos
- Valores actualizados en tiempo real

### Galería de Visualizaciones
- Grid responsive de imágenes
- Modal para vista ampliada
- Navegación intuitiva

### Output del Modelo
- Log completo del análisis
- Formato de consola
- Scroll automático

### Descarga de Reportes
- Exportación en formato texto
- Incluye todas las métricas
- Timestamp automático

## Troubleshooting

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

### La interfaz no carga los estilos

**Solución:** Asegúrate de que la estructura de carpetas esté intacta:
- `css/styles.css`
- `css/analisis.css`
- `js/main.js`
- `js/analisis.js`

### CORS Error en el navegador

**Solución:** El backend ya incluye flask-cors. Si persiste, verifica que app.py tenga:
```python
from flask_cors import CORS
CORS(app)
```

## Mejoras Futuras

- [ ] Upload de datasets personalizados
- [ ] Ajuste de hiperparámetros desde la interfaz
- [ ] Comparación de múltiples ejecuciones
- [ ] Exportación de reportes en PDF
- [ ] Gráficos interactivos (Plotly)
- [ ] Predicciones individuales
- [ ] Histórico de análisis
- [ ] Integración con Spotify API

## Tecnologías Utilizadas

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

## Licencia

Proyecto académico para el curso de Sistemas de Información.

## Contacto

Para preguntas o sugerencias sobre la interfaz, consulta con el equipo de desarrollo.

---

**Desarrollado con ❤️ para análisis de Machine Learning en Spotify**
