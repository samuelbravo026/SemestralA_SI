/**
 * SPOTIFY POPULARITY ANALYSIS - FRONTEND
 * JavaScript para interactuar con el backend Flask y mostrar resultados
 */

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
let analysisState = {
    isRunning: false,
    hasResults: false,
    currentResults: null
};

// DOM Elements
const elements = {
    runAnalysisBtn: document.getElementById('runAnalysisBtn'),
    viewResultsBtn: document.getElementById('viewResultsBtn'),
    downloadReportBtn: document.getElementById('downloadReportBtn'),
    statusBadge: document.getElementById('statusBadge'),
    progressContainer: document.getElementById('progressContainer'),
    progressFill: document.getElementById('progressFill'),
    progressText: document.getElementById('progressText'),
    resultsSection: document.getElementById('resultsSection'),
    imageGallery: document.getElementById('imageGallery'),
    modelOutput: document.getElementById('modelOutput'),
    toggleLogBtn: document.getElementById('toggleLogBtn'),
    logContainer: document.getElementById('logContainer'),
    imageModal: document.getElementById('imageModal'),
    modalImage: document.getElementById('modalImage'),
    modalCaption: document.getElementById('modalCaption'),
    closeModal: document.getElementById('closeModal'),
    // Metrics
    bestModel: document.getElementById('bestModel'),
    r2Score: document.getElementById('r2Score'),
    rmseScore: document.getElementById('rmseScore'),
    maeScore: document.getElementById('maeScore'),
    // Dataset Info
    datasetRecords: document.getElementById('datasetRecords'),
    datasetFeatures: document.getElementById('datasetFeatures')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Spotify Analysis Interface initialized');

    // Event Listeners
    elements.runAnalysisBtn.addEventListener('click', handleRunAnalysis);
    elements.viewResultsBtn.addEventListener('click', scrollToResults);
    elements.downloadReportBtn.addEventListener('click', handleDownloadReport);
    elements.toggleLogBtn.addEventListener('click', toggleLog);
    elements.closeModal.addEventListener('click', closeModal);

    // Check for existing results on load
    checkExistingResults();

    // Load dataset info
    loadDatasetInfo();
});

/**
 * Check if there are existing analysis results
 */
async function checkExistingResults() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        const data = await response.json();

        if (data.status === 'completed') {
            const resultsResponse = await fetch(`${API_BASE_URL}/results`);
            const results = await resultsResponse.json();

            analysisState.hasResults = true;
            analysisState.currentResults = results;

            displayResults(results);
            updateStatus('completed', 'Completado');
            elements.viewResultsBtn.disabled = false;
            elements.downloadReportBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error checking existing results:', error);
    }
}

/**
 * Load dataset information
 */
async function loadDatasetInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/dataset-info`);
        const data = await response.json();

        if (data.status === 'success') {
            elements.datasetRecords.textContent = data.info.total_records.toLocaleString();
            elements.datasetFeatures.textContent = data.info.features;
        }
    } catch (error) {
        console.error('Error loading dataset info:', error);
    }
}

/**
 * Handle Run Analysis button click
 */
async function handleRunAnalysis() {
    if (analysisState.isRunning) {
        showNotification('El análisis ya está en ejecución', 'warning');
        return;
    }

    if (!confirm('¿Deseas ejecutar el análisis completo? Esto puede tomar varios minutos.')) {
        return;
    }

    analysisState.isRunning = true;
    elements.runAnalysisBtn.disabled = true;
    elements.viewResultsBtn.disabled = true;
    elements.downloadReportBtn.disabled = true;

    updateStatus('running', 'Ejecutando...');
    showProgress(true);

    try {
        // Simulate progress
        simulateProgress();

        // Make API call
        const response = await fetch(`${API_BASE_URL}/run-analysis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Error en el servidor');
        }

        const data = await response.json();

        if (data.status === 'success') {
            analysisState.hasResults = true;
            analysisState.currentResults = data.results;

            setProgress(100, '¡Análisis completado!');
            updateStatus('completed', 'Completado');

            setTimeout(() => {
                displayResults(data.results);
                showProgress(false);
                elements.viewResultsBtn.disabled = false;
                elements.downloadReportBtn.disabled = false;
                showNotification('Análisis completado exitosamente', 'success');
                scrollToResults();
            }, 1000);
        } else {
            throw new Error(data.message || 'Error desconocido');
        }
    } catch (error) {
        console.error('Error running analysis:', error);
        updateStatus('error', 'Error');
        showProgress(false);
        showNotification('Error al ejecutar el análisis: ' + error.message, 'error');
    } finally {
        analysisState.isRunning = false;
        elements.runAnalysisBtn.disabled = false;
    }
}

/**
 * Display analysis results
 */
function displayResults(results) {
    // Show results section
    elements.resultsSection.style.display = 'block';

    // Display metrics
    if (results.metrics) {
        elements.bestModel.textContent = results.metrics.best_model || '-';
        elements.r2Score.textContent = results.metrics.test_r2
            ? results.metrics.test_r2.toFixed(4)
            : '-';
        elements.rmseScore.textContent = results.metrics.test_rmse
            ? results.metrics.test_rmse.toFixed(2)
            : '-';
        elements.maeScore.textContent = results.metrics.test_mae
            ? results.metrics.test_mae.toFixed(2)
            : '-';
    }

    // Display images
    if (results.images && results.images.length > 0) {
        displayImages(results.images);
    }

    // Display output
    if (results.output) {
        elements.modelOutput.textContent = results.output;
    }
}

/**
 * Display generated images in gallery
 */
function displayImages(images) {
    elements.imageGallery.innerHTML = '';

    images.forEach(image => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';

        const img = document.createElement('img');
        img.src = `${API_BASE_URL.replace('/api', '')}${image.path}`;
        img.alt = image.title;
        img.loading = 'lazy';

        const caption = document.createElement('div');
        caption.className = 'gallery-caption';
        caption.textContent = image.title;

        galleryItem.appendChild(img);
        galleryItem.appendChild(caption);

        // Click to open modal
        galleryItem.addEventListener('click', () => {
            openImageModal(img.src, image.title);
        });

        elements.imageGallery.appendChild(galleryItem);
    });
}

/**
 * Open image in modal
 */
function openImageModal(src, caption) {
    elements.modalImage.src = src;
    elements.modalCaption.textContent = caption;
    elements.imageModal.classList.add('active');
}

/**
 * Close image modal
 */
function closeModal() {
    elements.imageModal.classList.remove('active');
}

// Close modal on outside click
elements.imageModal.addEventListener('click', (e) => {
    if (e.target === elements.imageModal) {
        closeModal();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && elements.imageModal.classList.contains('active')) {
        closeModal();
    }
});

/**
 * Update status badge
 */
function updateStatus(status, text) {
    const statusDot = elements.statusBadge.querySelector('.status-dot');
    const statusText = elements.statusBadge.querySelector('.status-text');

    statusDot.className = `status-dot ${status}`;
    statusText.textContent = text;
}

/**
 * Show/hide progress bar
 */
function showProgress(show) {
    elements.progressContainer.style.display = show ? 'block' : 'none';
    if (!show) {
        setProgress(0, '');
    }
}

/**
 * Set progress bar value
 */
function setProgress(percent, text) {
    elements.progressFill.style.width = `${percent}%`;
    elements.progressText.textContent = text;
}

/**
 * Simulate progress for better UX
 */
function simulateProgress() {
    const stages = [
        { percent: 0, text: 'Inicializando análisis...' },
        { percent: 15, text: 'Cargando dataset...' },
        { percent: 25, text: 'Preparando datos...' },
        { percent: 40, text: 'Análisis exploratorio...' },
        { percent: 55, text: 'Entrenando modelos...' },
        { percent: 70, text: 'Evaluando métricas...' },
        { percent: 85, text: 'Generando visualizaciones...' },
        { percent: 95, text: 'Finalizando...' }
    ];

    let currentStage = 0;

    const interval = setInterval(() => {
        if (currentStage < stages.length && analysisState.isRunning) {
            setProgress(stages[currentStage].percent, stages[currentStage].text);
            currentStage++;
        } else {
            clearInterval(interval);
        }
    }, 3000); // Change every 3 seconds
}

/**
 * Scroll to results section
 */
function scrollToResults() {
    if (analysisState.hasResults) {
        elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Toggle log visibility
 */
function toggleLog() {
    const icon = elements.toggleLogBtn.querySelector('i');

    if (elements.logContainer.style.display === 'none') {
        elements.logContainer.style.display = 'block';
        icon.className = 'fas fa-chevron-up';
    } else {
        elements.logContainer.style.display = 'none';
        icon.className = 'fas fa-chevron-down';
    }
}

/**
 * Handle download report
 */
function handleDownloadReport() {
    if (!analysisState.hasResults) {
        showNotification('No hay resultados para descargar', 'warning');
        return;
    }

    // Create a text report
    const report = generateTextReport(analysisState.currentResults);

    // Download as text file
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `spotify_analysis_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Reporte descargado exitosamente', 'success');
}

/**
 * Generate text report from results
 */
function generateTextReport(results) {
    const timestamp = new Date(results.timestamp).toLocaleString('es-ES');

    let report = `SPOTIFY POPULARITY ANALYSIS - REPORTE
${'='.repeat(80)}

Fecha de análisis: ${timestamp}
Estado: ${results.status}

`;

    if (results.metrics) {
        report += `MÉTRICAS PRINCIPALES
${'-'.repeat(80)}

Mejor Modelo: ${results.metrics.best_model || 'N/A'}
R² Score (Test): ${results.metrics.test_r2 ? results.metrics.test_r2.toFixed(4) : 'N/A'}
RMSE (Test): ${results.metrics.test_rmse ? results.metrics.test_rmse.toFixed(2) : 'N/A'}
MAE (Test): ${results.metrics.test_mae ? results.metrics.test_mae.toFixed(2) : 'N/A'}

`;
    }

    if (results.images && results.images.length > 0) {
        report += `VISUALIZACIONES GENERADAS
${'-'.repeat(80)}

`;
        results.images.forEach((img, i) => {
            report += `${i + 1}. ${img.title}\n`;
        });
        report += '\n';
    }

    if (results.output) {
        report += `OUTPUT COMPLETO DEL MODELO
${'-'.repeat(80)}

${results.output}
`;
    }

    return report;
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 9999;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 4000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Handle API connection errors
window.addEventListener('unhandledrejection', (event) => {
    if (event.reason instanceof TypeError && event.reason.message.includes('fetch')) {
        showNotification('No se puede conectar al servidor API. Asegúrate de que Flask esté ejecutándose.', 'error');
    }
});

console.log('Spotify Analysis Interface ready');
