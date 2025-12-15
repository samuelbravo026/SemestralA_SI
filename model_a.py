"""
SPOTIFY MUSIC POPULARITY ANALYSIS - UNIFIED PIPELINE
Complete Machine Learning Workflow
Dataset: Top Spotify Songs in 73 Countries

Pipeline Stages:
4.1 Data Preparation
4.2 Exploratory Data Analysis
5. Build Initial AI Model
6. Develop a Benchmark
7. Evaluate Primary Metrics
8. Evaluate Secondary Metrics
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, ttest_ind, mannwhitneyu
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (mean_squared_error, r2_score, mean_absolute_error,
                            mean_absolute_percentage_error, explained_variance_score)
import time
import psutil
import sys
import warnings
warnings.filterwarnings('ignore')

# Configure UTF-8 encoding for Windows compatibility
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ============================================================================
# CONFIGURATION
# ============================================================================

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

print("="*80)
print("SPOTIFY MUSIC POPULARITY ANALYSIS - UNIFIED PIPELINE")
print("="*80)
print("\nPipeline Stages:")
print("  4.1 Data Preparation")
print("  4.2 Exploratory Data Analysis")
print("  5. Build Initial AI Model")
print("  6. Develop a Benchmark")
print("  7. Evaluate Primary Metrics")
print("  8. Evaluate Secondary Metrics")
print("="*80)

# ============================================================================
# STAGE 4.1: DATA PREPARATION
# ============================================================================

print("\n" + "="*80)
print("STAGE 4.1: DATA PREPARATION")
print("="*80)

try:
    df = pd.read_csv('universal_top_spotify_songs.csv')
    print("\n✓ Dataset cargado exitosamente desde universal_top_spotify_songs.csv")
except FileNotFoundError:
    print("\n⚠ Archivo no encontrado. Creando dataset de ejemplo...")
    n_samples = 1000
    
    df = pd.DataFrame({
        'spotify_id': [f'track_{i}' for i in range(n_samples)],
        'name': [f'Song {i}' for i in range(n_samples)],
        'artists': [f'Artist {i%100}' for i in range(n_samples)],
        'popularity': np.random.randint(0, 101, n_samples),
        'is_explicit': np.random.choice([True, False], n_samples, p=[0.35, 0.65]),
        'danceability': np.random.uniform(0, 1, n_samples),
        'energy': np.random.uniform(0, 1, n_samples),
        'valence': np.random.uniform(0, 1, n_samples),
        'acousticness': np.random.uniform(0, 1, n_samples),
        'instrumentalness': np.random.uniform(0, 0.3, n_samples),
        'liveness': np.random.uniform(0, 0.4, n_samples),
        'speechiness': np.random.uniform(0, 0.5, n_samples),
        'loudness': np.random.uniform(-60, 0, n_samples),
        'tempo': np.random.uniform(60, 200, n_samples),
    })
    
    # Crear correlaciones realistas
    df['popularity'] = (
        40 + 
        15 * df['danceability'] + 
        10 * df['energy'] + 
        8 * df['valence'] - 
        5 * df['is_explicit'].astype(int) +
        np.random.normal(0, 10, n_samples)
    ).clip(0, 100)

print(f"Dimensiones del dataset: {df.shape}")

# Crear variable numérica para is_explicit
df['is_explicit_num'] = df['is_explicit'].astype(int)

# Análisis de calidad de datos
print("\n" + "-"*80)
print("ANÁLISIS DE CALIDAD DE DATOS")
print("-"*80)

null_counts = df.isnull().sum()
print(f"\nValores nulos: {null_counts.sum()}")
if null_counts.sum() == 0:
    print("✓ No se encontraron valores nulos")

duplicates = df.duplicated().sum()
print(f"Filas duplicadas: {duplicates}")
if duplicates == 0:
    print("✓ No se encontraron duplicados")

# Guardar datos procesados
df.to_csv('data_processed_clean.csv', index=False)
print("\n✓ Datos procesados guardados: data_processed_clean.csv")

# ============================================================================
# STAGE 4.2: EXPLORATORY DATA ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("STAGE 4.2: EXPLORATORY DATA ANALYSIS")
print("="*80)

# 1. ANÁLISIS UNIVARIADO - POPULARITY
print("\n1. ANÁLISIS UNIVARIADO - VARIABLE DEPENDIENTE (Popularity)")
print("-"*80)

print(f"\nEstadísticas de Popularity:")
print(f"  Media: {df['popularity'].mean():.2f}")
print(f"  Mediana: {df['popularity'].median():.2f}")
print(f"  Desviación estándar: {df['popularity'].std():.2f}")
print(f"  Mínimo: {df['popularity'].min():.2f}")
print(f"  Máximo: {df['popularity'].max():.2f}")

skewness = df['popularity'].skew()
kurtosis = df['popularity'].kurtosis()
shapiro_stat, shapiro_p = shapiro(df['popularity'].sample(min(5000, len(df))))

print(f"\n  Asimetría (Skewness): {skewness:.3f}")
print(f"  Curtosis: {kurtosis:.3f}")
print(f"  Test de Shapiro-Wilk: p-valor = {shapiro_p:.4f}")
print(f"  → Distribución: {'Normal' if shapiro_p >= 0.05 else 'No Normal'}")

# VISUALIZACIÓN 1: Distribución de Popularity
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].hist(df['popularity'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].axvline(df['popularity'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Media: {df["popularity"].mean():.1f}')
axes[0].axvline(df['popularity'].median(), color='green', linestyle='--', linewidth=2, 
                label=f'Mediana: {df["popularity"].median():.1f}')
axes[0].set_xlabel('Popularity', fontsize=12)
axes[0].set_ylabel('Frecuencia', fontsize=12)
axes[0].set_title('Distribución de Popularity', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].boxplot(df['popularity'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=2))
axes[1].set_ylabel('Popularity', fontsize=12)
axes[1].set_title('Box Plot de Popularity', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

df['popularity'].plot(kind='density', ax=axes[2], color='steelblue', linewidth=2)
axes[2].set_xlabel('Popularity', fontsize=12)
axes[2].set_ylabel('Densidad', fontsize=12)
axes[2].set_title('Distribución de Densidad', fontsize=14, fontweight='bold')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_popularity_distribution.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 01_popularity_distribution.png")
plt.close()

# 2. ANÁLISIS BIVARIADO - EXPLICIT VS POPULARITY
print("\n2. ANÁLISIS BIVARIADO - EXPLICIT VS POPULARITY")
print("-"*80)

explicit_group = df[df['is_explicit_num'] == 1]['popularity']
non_explicit_group = df[df['is_explicit_num'] == 0]['popularity']

print(f"\nNo Explicit (N={len(non_explicit_group)}):")
print(f"  Media: {non_explicit_group.mean():.2f}")
print(f"  Mediana: {non_explicit_group.median():.2f}")

print(f"\nExplicit (N={len(explicit_group)}):")
print(f"  Media: {explicit_group.mean():.2f}")
print(f"  Mediana: {explicit_group.median():.2f}")

mean_diff = explicit_group.mean() - non_explicit_group.mean()
print(f"\nDiferencia de medias: {mean_diff:.2f} puntos")

# Pruebas estadísticas
t_stat, t_pvalue = ttest_ind(explicit_group, non_explicit_group)
u_stat, u_pvalue = mannwhitneyu(explicit_group, non_explicit_group)

pooled_std = np.sqrt(((len(explicit_group)-1)*explicit_group.std()**2 + 
                    (len(non_explicit_group)-1)*non_explicit_group.std()**2) / 
                    (len(explicit_group) + len(non_explicit_group) - 2))
cohens_d = mean_diff / pooled_std

print(f"\nPruebas estadísticas:")
print(f"  Test t: t={t_stat:.3f}, p={t_pvalue:.4f}")
print(f"  Mann-Whitney U: U={u_stat:.0f}, p={u_pvalue:.4f}")
print(f"  Cohen's d: {cohens_d:.3f}")
print(f"\n  → {'EXISTE' if t_pvalue < 0.05 else 'NO EXISTE'} diferencia significativa (p < 0.05)")

# VISUALIZACIÓN 2: Comparación Explicit vs Non-Explicit
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

explicit_counts = df['is_explicit_num'].value_counts()
axes[0, 0].bar(['No Explicit', 'Explicit'], 
            [explicit_counts[0], explicit_counts[1]], 
            color=['steelblue', 'coral'], edgecolor='black', alpha=0.7)
axes[0, 0].set_ylabel('Frecuencia', fontsize=12)
axes[0, 0].set_title('Distribución por Contenido Explícito', fontsize=14, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3, axis='y')

box_data = [non_explicit_group, explicit_group]
bp = axes[0, 1].boxplot(box_data, labels=['No Explicit', 'Explicit'], 
                        patch_artist=True, widths=0.6)
for patch, color in zip(bp['boxes'], ['steelblue', 'coral']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0, 1].set_ylabel('Popularity', fontsize=12)
axes[0, 1].set_title('Box Plot: Popularity por Contenido', fontsize=14, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='y')

parts = axes[1, 0].violinplot([non_explicit_group, explicit_group], 
                            positions=[1, 2], showmeans=True, showmedians=True)
for pc, color in zip(parts['bodies'], ['steelblue', 'coral']):
    pc.set_facecolor(color)
    pc.set_alpha(0.7)
axes[1, 0].set_xticks([1, 2])
axes[1, 0].set_xticklabels(['No Explicit', 'Explicit'])
axes[1, 0].set_ylabel('Popularity', fontsize=12)
axes[1, 0].set_title('Violin Plot: Distribución de Popularity', fontsize=14, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3, axis='y')

axes[1, 1].hist(non_explicit_group, bins=30, alpha=0.6, label='No Explicit', 
                color='steelblue', edgecolor='black')
axes[1, 1].hist(explicit_group, bins=30, alpha=0.6, label='Explicit', 
                color='coral', edgecolor='black')
axes[1, 1].axvline(non_explicit_group.mean(), color='blue', linestyle='--', linewidth=2)
axes[1, 1].axvline(explicit_group.mean(), color='red', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Popularity', fontsize=12)
axes[1, 1].set_ylabel('Frecuencia', fontsize=12)
axes[1, 1].set_title('Distribución Comparativa', fontsize=14, fontweight='bold')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('02_explicit_vs_popularity.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: 02_explicit_vs_popularity.png")
plt.close()

# 3. MATRIZ DE CORRELACIÓN
print("\n3. MATRIZ DE CORRELACIÓN")
print("-"*80)

numeric_features = ['popularity', 'is_explicit_num', 'danceability', 'energy', 
                    'valence', 'acousticness', 'instrumentalness', 'liveness', 
                    'speechiness', 'loudness', 'tempo']
numeric_features = [col for col in numeric_features if col in df.columns]
correlation_matrix = df[numeric_features].corr()

popularity_corr = correlation_matrix['popularity'].sort_values(ascending=False)
print("\nCorrelaciones con Popularity (|r| > 0.1):")
for feature, corr in popularity_corr.items():
    if feature != 'popularity' and abs(corr) > 0.1:
        print(f"  {feature:20s}: {corr:+.3f}")

# VISUALIZACIÓN 3: Matriz de correlación
fig, ax = plt.subplots(figsize=(14, 10))
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(correlation_matrix, mask=mask, annot=True, fmt='.2f', 
            cmap='coolwarm', center=0, square=True, linewidths=1, 
            cbar_kws={"shrink": 0.8}, ax=ax, vmin=-1, vmax=1)
ax.set_title('Matriz de Correlación', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('03_correlation_matrix.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 03_correlation_matrix.png")
plt.close()

# ============================================================================
# STAGE 5: BUILD INITIAL AI MODEL
# ============================================================================

print("\n" + "="*80)
print("STAGE 5: BUILD INITIAL AI MODEL")
print("="*80)

# Preparar datos
feature_cols = ['is_explicit_num', 'danceability', 'energy', 'valence', 
                'acousticness', 'instrumentalness', 'liveness', 'speechiness',
                'loudness', 'tempo']
feature_cols = [col for col in feature_cols if col in df.columns]

X = df[feature_cols].fillna(df[feature_cols].median())
y = df['popularity']

print(f"\nFeatures: {len(feature_cols)}")
print(f"Dimensiones X: {X.shape}, y: {y.shape}")

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

print(f"\nTrain: {X_train.shape[0]} muestras ({len(X_train)/len(X)*100:.1f}%)")
print(f"Test: {X_test.shape[0]} muestras ({len(X_test)/len(X)*100:.1f}%)")

# Estandarización
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n✓ Features estandarizados")

# Entrenar modelos
models = {}
results = []

print("\nEntrenando modelos...")

# Linear Regression
print("  • Linear Regression...", end='')
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)
models['Linear Regression'] = lr_model
y_pred_train_lr = lr_model.predict(X_train_scaled)
y_pred_test_lr = lr_model.predict(X_test_scaled)
results.append({
    'Model': 'Linear Regression',
    'Train RMSE': np.sqrt(mean_squared_error(y_train, y_pred_train_lr)),
    'Test RMSE': np.sqrt(mean_squared_error(y_test, y_pred_test_lr)),
    'Train R²': r2_score(y_train, y_pred_train_lr),
    'Test R²': r2_score(y_test, y_pred_test_lr),
    'MAE': mean_absolute_error(y_test, y_pred_test_lr)
})
print(" ✓")

# Ridge Regression
print("  • Ridge Regression...", end='')
ridge_model = Ridge(alpha=1.0, random_state=RANDOM_STATE)
ridge_model.fit(X_train_scaled, y_train)
models['Ridge'] = ridge_model
y_pred_test_ridge = ridge_model.predict(X_test_scaled)
results.append({
    'Model': 'Ridge Regression',
    'Train RMSE': np.sqrt(mean_squared_error(y_train, ridge_model.predict(X_train_scaled))),
    'Test RMSE': np.sqrt(mean_squared_error(y_test, y_pred_test_ridge)),
    'Train R²': r2_score(y_train, ridge_model.predict(X_train_scaled)),
    'Test R²': r2_score(y_test, y_pred_test_ridge),
    'MAE': mean_absolute_error(y_test, y_pred_test_ridge)
})
print(" ✓")

# Random Forest
print("  • Random Forest...", end='')
rf_model = RandomForestRegressor(
    n_estimators=100, max_depth=10, min_samples_split=10,
    random_state=RANDOM_STATE, n_jobs=-1
)
rf_model.fit(X_train_scaled, y_train)
models['Random Forest'] = rf_model
y_pred_train_rf = rf_model.predict(X_train_scaled)
y_pred_test_rf = rf_model.predict(X_test_scaled)
results.append({
    'Model': 'Random Forest',
    'Train RMSE': np.sqrt(mean_squared_error(y_train, y_pred_train_rf)),
    'Test RMSE': np.sqrt(mean_squared_error(y_test, y_pred_test_rf)),
    'Train R²': r2_score(y_train, y_pred_train_rf),
    'Test R²': r2_score(y_test, y_pred_test_rf),
    'MAE': mean_absolute_error(y_test, y_pred_test_rf)
})
print(" ✓")

# Gradient Boosting
print("  • Gradient Boosting...", end='')
gb_model = GradientBoostingRegressor(
    n_estimators=100, learning_rate=0.1, max_depth=5, random_state=RANDOM_STATE
)
gb_model.fit(X_train_scaled, y_train)
models['Gradient Boosting'] = gb_model
y_pred_test_gb = gb_model.predict(X_test_scaled)
results.append({
    'Model': 'Gradient Boosting',
    'Train RMSE': np.sqrt(mean_squared_error(y_train, gb_model.predict(X_train_scaled))),
    'Test RMSE': np.sqrt(mean_squared_error(y_test, y_pred_test_gb)),
    'Train R²': r2_score(y_train, gb_model.predict(X_train_scaled)),
    'Test R²': r2_score(y_test, y_pred_test_gb),
    'MAE': mean_absolute_error(y_test, y_pred_test_gb)
})
print(" ✓")

# Comparación de modelos
results_df = pd.DataFrame(results)
print("\n" + "-"*80)
print("COMPARACIÓN DE MODELOS")
print("-"*80)
print(results_df.to_string(index=False))

best_model_name = results_df.loc[results_df['Test R²'].idxmax(), 'Model']
best_r2 = results_df['Test R²'].max()
print(f"\n🏆 MEJOR MODELO: {best_model_name} (R² = {best_r2:.4f})")

# Importancia de features
print("\n" + "-"*80)
print("IMPORTANCIA DE FEATURES")
print("-"*80)

rf_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nRandom Forest Feature Importance:")
print(rf_importance.to_string(index=False))

explicit_importance = rf_importance[rf_importance['Feature'] == 'is_explicit_num']['Importance'].values[0]
explicit_rank = rf_importance.reset_index().loc[
    rf_importance.reset_index()['Feature'] == 'is_explicit_num', 'index'
].values[0] + 1

print(f"\nis_explicit_num:")
print(f"  Importancia: {explicit_importance:.4f}")
print(f"  Ranking: {explicit_rank}° de {len(feature_cols)}")

# VISUALIZACIÓN 4: Feature Importance
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(rf_importance['Feature'], rf_importance['Importance'], color='steelblue', alpha=0.7)
ax.set_xlabel('Importancia', fontsize=12)
ax.set_title('Feature Importance - Random Forest', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('04_feature_importance.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 04_feature_importance.png")
plt.close()

# ============================================================================
# STAGE 6 & 7: BENCHMARK AND PRIMARY METRICS
# ============================================================================

print("\n" + "="*80)
print("STAGE 6 & 7: BENCHMARK AND PRIMARY METRICS")
print("="*80)

# Usar mejor modelo para evaluación
best_model = models[best_model_name]
y_pred_train_best = best_model.predict(X_train_scaled)
y_pred_test_best = best_model.predict(X_test_scaled)

# Métricas primarias
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train_best))
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test_best))
train_mae = mean_absolute_error(y_train, y_pred_train_best)
test_mae = mean_absolute_error(y_test, y_pred_test_best)
train_r2 = r2_score(y_train, y_pred_train_best)
test_r2 = r2_score(y_test, y_pred_test_best)
train_mape = mean_absolute_percentage_error(y_train.replace(0, 0.1), y_pred_train_best) * 100
test_mape = mean_absolute_percentage_error(y_test.replace(0, 0.1), y_pred_test_best) * 100

primary_metrics = pd.DataFrame({
    'Metric': ['RMSE', 'MAE', 'R²', 'MAPE (%)'],
    'Train': [train_rmse, train_mae, train_r2, train_mape],
    'Test': [test_rmse, test_mae, test_r2, test_mape]
})

print("\nMÉTRICAS PRIMARIAS:")
print("-"*80)
print(primary_metrics.to_string(index=False))

print("\n" + "-"*80)
print("INTERPRETACIÓN:")
print("-"*80)
print(f"✓ R² Test = {test_r2:.4f}: Explica el {test_r2*100:.2f}% de la varianza")
print(f"✓ RMSE Test = {test_rmse:.2f}: Error promedio de {test_rmse:.2f} puntos")
print(f"✓ MAE Test = {test_mae:.2f}: Error absoluto promedio")

overfitting_gap = train_r2 - test_r2
print(f"\nGap R² (Train - Test): {overfitting_gap:.4f}")
if overfitting_gap < 0.05:
    print("  → Bajo riesgo de overfitting ✓")
elif overfitting_gap < 0.15:
    print("  → Overfitting moderado ⚠")
else:
    print("  → Alto overfitting ⚠⚠")

# Análisis de residuales
train_residuals = y_train - y_pred_train_best
test_residuals = y_test - y_pred_test_best

threshold_residuals = 3 * test_residuals.std()
anomalous_predictions = np.abs(test_residuals) > threshold_residuals

print("\n" + "-"*80)
print("BENCHMARK - DETECCIÓN DE ANOMALÍAS:")
print("-"*80)
print(f"Predicciones anómalas: {anomalous_predictions.sum()} de {len(test_residuals)}")
print(f"Porcentaje: {(anomalous_predictions.sum()/len(test_residuals)*100):.2f}%")

# ============================================================================
# STAGE 8: SECONDARY METRICS
# ============================================================================

print("\n" + "="*80)
print("STAGE 8: SECONDARY METRICS")
print("="*80)

# Rendimiento computacional
print("\n1. RENDIMIENTO COMPUTACIONAL:")
print("-"*80)

start_time = time.time()
rf_temp = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=RANDOM_STATE, n_jobs=-1)
rf_temp.fit(X_train_scaled, y_train)
training_time = time.time() - start_time

start_time = time.time()
_ = rf_temp.predict(X_test_scaled)
prediction_time = time.time() - start_time

print(f"Tiempo de entrenamiento: {training_time:.4f} segundos")
print(f"Tiempo de predicción: {prediction_time:.4f} segundos")

# Memoria
process = psutil.Process()
memory_mb = process.memory_info().rss / (1024 * 1024)
model_size_kb = sys.getsizeof(best_model) / 1024

print(f"\n2. RENDIMIENTO DE MEMORIA:")
print("-"*80)
print(f"Uso de memoria: {memory_mb:.2f} MB")
print(f"Tamaño del modelo: {model_size_kb:.2f} KB")

# Implicaciones éticas
print(f"\n3. IMPLICACIONES ÉTICAS:")
print("-"*80)

if 'is_explicit_num' in X_test.columns:
    explicit_mask = X_test['is_explicit_num'] == 1
    pred_explicit = y_pred_test_best[explicit_mask]
    pred_non_explicit = y_pred_test_best[~explicit_mask]
    
    pred_mean_diff = pred_explicit.mean() - pred_non_explicit.mean()
    
    print(f"Predicción promedio (Explicit): {pred_explicit.mean():.2f}")
    print(f"Predicción promedio (Non-Explicit): {pred_non_explicit.mean():.2f}")
    print(f"Diferencia: {pred_mean_diff:.2f} puntos")
    
    if abs(pred_mean_diff) < 2:
        print("  → Equidad aceptable ✓")
    elif abs(pred_mean_diff) < 5:
        print("  → Diferencia moderada - revisar ⚠")
    else:
        print("  → Posible sesgo - revisar ⚠⚠")

# Robustez
print(f"\n4. ROBUSTEZ DEL MODELO:")
print("-"*80)

noise_levels = [0, 0.01, 0.05, 0.1]
robustness_results = []

for noise in noise_levels:
    if noise == 0:
        X_noisy = X_test_scaled
    else:
        X_noisy = X_test_scaled + np.random.normal(0, noise, X_test_scaled.shape)
    
    y_pred_noisy = best_model.predict(X_noisy)
    r2_noisy = r2_score(y_test, y_pred_noisy)
    
    robustness_results.append({
        'Noise Level': f"{noise*100:.1f}%",
        'R²': r2_noisy,
        'R² Drop': test_r2 - r2_noisy
    })
    print(f"Ruido {noise*100:.1f}%: R² = {r2_noisy:.4f} (caída: {test_r2 - r2_noisy:.4f})")

robustness_df = pd.DataFrame(robustness_results)

# VISUALIZACIÓN 5: Métricas y Evaluación Completa
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Residuales
axes[0, 0].scatter(y_pred_test_best, test_residuals, alpha=0.5, s=20)
axes[0, 0].axhline(y=0, color='r', linestyle='--', lw=2)
axes[0, 0].axhline(y=threshold_residuals, color='orange', linestyle=':', lw=1, label='Umbral anomalía')
axes[0, 0].axhline(y=-threshold_residuals, color='orange', linestyle=':', lw=1)
axes[0, 0].set_xlabel('Predicción')
axes[0, 0].set_ylabel('Residual')
axes[0, 0].set_title('Análisis de Residuales', fontsize=14, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Distribución de errores
axes[0, 1].hist(np.abs(test_residuals), bins=30, edgecolor='black', alpha=0.7, color='steelblue')
axes[0, 1].set_xlabel('Error Absoluto')
axes[0, 1].set_ylabel('Frecuencia')
axes[0, 1].set_title('Distribución de Errores Absolutos', fontsize=14, fontweight='bold')
axes[0, 1].axvline(test_mae, color='r', linestyle='--', label=f'MAE: {test_mae:.2f}')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Comparación Train vs Test
metrics_names = ['RMSE', 'MAE', 'R²']
train_values = [train_rmse, train_mae, train_r2]
test_values = [test_rmse, test_mae, test_r2]

x_pos = np.arange(len(metrics_names))
width = 0.35

axes[1, 0].bar(x_pos - width/2, train_values, width, label='Train', alpha=0.8, color='steelblue')
axes[1, 0].bar(x_pos + width/2, test_values, width, label='Test', alpha=0.8, color='coral')
axes[1, 0].set_xlabel('Métrica')
axes[1, 0].set_ylabel('Valor')
axes[1, 0].set_title('Comparación Train vs Test', fontsize=14, fontweight='bold')
axes[1, 0].set_xticks(x_pos)
axes[1, 0].set_xticklabels(metrics_names)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Robustez ante ruido
noise_levels_plot = [float(r['Noise Level'].strip('%')) for r in robustness_results]
r2_values = [r['R²'] for r in robustness_results]

axes[1, 1].plot(noise_levels_plot, r2_values, marker='o', linewidth=2, markersize=8, color='steelblue')
axes[1, 1].set_xlabel('Nivel de Ruido (%)')
axes[1, 1].set_ylabel('R²')
axes[1, 1].set_title('Robustez: Efecto del Ruido en R²', fontsize=14, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].axhline(y=test_r2*0.9, color='r', linestyle='--', alpha=0.5, label='90% R² original')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('05_metrics_evaluation.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 05_metrics_evaluation.png")
plt.close()

# VISUALIZACIÓN 6: Predicciones vs Valores Reales
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scatter plot
axes[0].scatter(y_test, y_pred_test_best, alpha=0.5, s=30, color='steelblue', edgecolors='black', linewidth=0.5)
axes[0].plot([y_test.min(), y_test.max()], 
            [y_test.min(), y_test.max()], 
            'r--', lw=2, label='Predicción perfecta')
axes[0].set_xlabel('Popularity Real', fontsize=12)
axes[0].set_ylabel('Popularity Predicha', fontsize=12)
axes[0].set_title(f'Predicciones: {best_model_name}', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].text(0.05, 0.95, f'R² = {test_r2:.4f}\nRMSE = {test_rmse:.2f}',
            transform=axes[0].transAxes, ha='left', va='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Residuales con colores
scatter = axes[1].scatter(y_pred_test_best, test_residuals, 
                        c=np.abs(test_residuals), cmap='YlOrRd', 
                        alpha=0.6, s=30, edgecolors='black', linewidth=0.5)
axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
axes[1].set_xlabel('Popularity Predicha', fontsize=12)
axes[1].set_ylabel('Residuales', fontsize=12)
axes[1].set_title('Análisis de Residuales', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)
plt.colorbar(scatter, ax=axes[1], label='|Error|')

plt.tight_layout()
plt.savefig('06_predictions_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: 06_predictions_analysis.png")
plt.close()

# ============================================================================
# RESUMEN FINAL COMPLETO
# ============================================================================

print("\n" + "="*80)
print("RESUMEN FINAL - SPOTIFY POPULARITY ANALYSIS")
print("="*80)

print(f"""
═══════════════════════════════════════════════════════════════════════════

📊 DATASET
• Total de registros: {len(df):,}
• Features utilizados: {len(feature_cols)}
• Train/Test split: 80/20

═══════════════════════════════════════════════════════════════════════════

📈 ANÁLISIS EXPLORATORIO
• Media Popularity: {df['popularity'].mean():.2f}
• Distribución: {'Normal' if shapiro_p >= 0.05 else 'No Normal'}
• Diferencia Explicit vs Non-Explicit: {mean_diff:.2f} puntos
• Significancia estadística: {'SÍ (p < 0.05)' if t_pvalue < 0.05 else 'NO (p ≥ 0.05)'}
• Cohen's d: {cohens_d:.3f}

═══════════════════════════════════════════════════════════════════════════

🤖 MODELOS ENTRENADOS
• Linear Regression
• Ridge Regression
• Random Forest Regressor
• Gradient Boosting Regressor

🏆 MEJOR MODELO: {best_model_name}
• Test R²: {test_r2:.4f} ({test_r2*100:.2f}% de varianza explicada)
• Test RMSE: {test_rmse:.2f} puntos
• Test MAE: {test_mae:.2f} puntos
• Test MAPE: {test_mape:.2f}%

═══════════════════════════════════════════════════════════════════════════

🎯 VARIABLE DE INTERÉS: is_explicit_num
• Importancia en Random Forest: {explicit_importance:.4f}
• Ranking: {explicit_rank}° de {len(feature_cols)} features
• Efecto en predicción: {pred_mean_diff:.2f} puntos de diferencia

═══════════════════════════════════════════════════════════════════════════

⚡ MÉTRICAS SECUNDARIAS

1. RENDIMIENTO COMPUTACIONAL:
• Tiempo entrenamiento: {training_time:.4f}s
• Tiempo predicción: {prediction_time:.4f}s

2. MEMORIA:
• Uso de proceso: {memory_mb:.2f} MB
• Tamaño del modelo: {model_size_kb:.2f} KB

3. ROBUSTEZ:
• R² con ruido 0%: {robustness_results[0]['R²']:.4f}
• R² con ruido 10%: {robustness_results[-1]['R²']:.4f}
• Caída: {robustness_results[-1]['R² Drop']:.4f}
• Estado: {'✓ Robusto' if robustness_results[-1]['R² Drop'] < 0.1 else '⚠ Moderado'}

4. EQUIDAD:
• Diferencia predicción Explicit/Non-Explicit: {pred_mean_diff:.2f} puntos
• Evaluación: {'✓ Equitativo' if abs(pred_mean_diff) < 2 else '⚠ Revisar'}

5. ANOMALÍAS DETECTADAS:
• Predicciones anómalas: {anomalous_predictions.sum()} ({anomalous_predictions.sum()/len(test_residuals)*100:.2f}%)
• Umbral: ±{threshold_residuals:.2f}

═══════════════════════════════════════════════════════════════════════════

📁 ARCHIVOS GENERADOS
✓ data_processed_clean.csv - Dataset procesado
✓ 01_popularity_distribution.png - Distribución de popularidad
✓ 02_explicit_vs_popularity.png - Comparación Explicit vs Non-Explicit
✓ 03_correlation_matrix.png - Matriz de correlación
✓ 04_feature_importance.png - Importancia de features
✓ 05_metrics_evaluation.png - Evaluación completa de métricas
✓ 06_predictions_analysis.png - Análisis de predicciones

═══════════════════════════════════════════════════════════════════════════

✅ PIPELINE COMPLETADO EXITOSAMENTE

═══════════════════════════════════════════════════════════════════════════
""")

print("\n" + "="*80)
print("CONCLUSIONES PRINCIPALES")
print("="*80)

print(f"""
1. El modelo {best_model_name} demostró el mejor rendimiento con un R² de {test_r2:.4f},
explicando {test_r2*100:.2f}% de la varianza en la popularidad de las canciones.

2. La variable 'is_explicit' ocupa el {explicit_rank}° lugar en importancia, con un
valor de {explicit_importance:.4f}, lo que indica {'una contribución significativa' if explicit_rank <= 3 else 'una contribución moderada'} 
a la predicción de popularidad.

3. {'Existe una diferencia estadísticamente significativa' if t_pvalue < 0.05 else 'No existe una diferencia estadísticamente significativa'}
(p = {t_pvalue:.4f}) en la popularidad entre canciones con y sin contenido explícito,
con una diferencia promedio de {mean_diff:.2f} puntos.

4. El modelo muestra {'bajo riesgo de overfitting' if overfitting_gap < 0.05 else 'overfitting moderado' if overfitting_gap < 0.15 else 'alto overfitting'}
con un gap de R² de {overfitting_gap:.4f} entre train y test.

5. El sistema es {'robusto' if robustness_results[-1]['R² Drop'] < 0.1 else 'moderadamente robusto'} ante ruido en los datos,
manteniendo un R² de {robustness_results[-1]['R²']:.4f} incluso con 10% de ruido.

6. El análisis de equidad muestra {'una distribución equitativa' if abs(pred_mean_diff) < 2 else 'una diferencia moderada'}
en las predicciones entre contenido explícito y no explícito.
""")

print("="*80)
print("FIN DEL PIPELINE")
print("="*80)