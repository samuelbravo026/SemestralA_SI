"""
Flask API Backend for Spotify Popularity Analysis Model
Provides endpoints to run the ML model and retrieve results
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import subprocess
import os
import json
import pandas as pd
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# Store the latest analysis results
latest_results = {
    'status': 'idle',
    'timestamp': None,
    'metrics': None,
    'model_info': None,
    'dataset_info': None
}

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'Spotify Popularity Analysis API',
        'endpoints': [
            '/api/run-analysis',
            '/api/status',
            '/api/results',
            '/api/images/<image_name>'
        ]
    })

@app.route('/api/run-analysis', methods=['POST'])
def run_analysis():
    """Execute the model_a.py script and return results"""
    global latest_results

    try:
        # Update status
        latest_results['status'] = 'running'
        latest_results['timestamp'] = datetime.now().isoformat()

        # Run the model script
        print("Starting analysis...")
        result = subprocess.run(
            ['python', 'model_a.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        if result.returncode != 0:
            latest_results['status'] = 'error'
            return jsonify({
                'status': 'error',
                'message': 'Error running model',
                'error': result.stderr
            }), 500

        # Parse results from output
        output = result.stdout

        # Extract key metrics from output
        metrics = extract_metrics_from_output(output)

        # Check if images were generated
        images = []
        for i in range(1, 7):
            img_path = f'0{i}_*.png'
            if os.path.exists(img_path.replace('*', '')):
                images.append(img_path)

        # Update results
        latest_results = {
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'images': check_generated_images(),
            'output': output
        }

        return jsonify({
            'status': 'success',
            'message': 'Analysis completed successfully',
            'results': latest_results
        })

    except subprocess.TimeoutExpired:
        latest_results['status'] = 'error'
        return jsonify({
            'status': 'error',
            'message': 'Analysis timeout (exceeded 5 minutes)'
        }), 500

    except Exception as e:
        latest_results['status'] = 'error'
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current analysis status"""
    return jsonify({
        'status': latest_results['status'],
        'timestamp': latest_results['timestamp']
    })

@app.route('/api/results', methods=['GET'])
def get_results():
    """Get latest analysis results"""
    if latest_results['status'] == 'idle':
        return jsonify({
            'status': 'idle',
            'message': 'No analysis has been run yet'
        })

    return jsonify(latest_results)

@app.route('/api/images/<image_name>', methods=['GET'])
def get_image(image_name):
    """Serve generated images"""
    try:
        image_path = os.path.join(os.getcwd(), image_name)
        if os.path.exists(image_path):
            return send_file(image_path, mimetype='image/png')
        else:
            return jsonify({
                'status': 'error',
                'message': 'Image not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/dataset-info', methods=['GET'])
def get_dataset_info():
    """Get information about the dataset"""
    try:
        # Try to read the processed data
        if os.path.exists('data_processed_clean.csv'):
            df = pd.read_csv('data_processed_clean.csv')
            return jsonify({
                'status': 'success',
                'info': {
                    'total_records': len(df),
                    'columns': list(df.columns),
                    'features': len(df.columns),
                    'file_size': os.path.getsize('data_processed_clean.csv')
                }
            })
        else:
            return jsonify({
                'status': 'info',
                'message': 'No processed dataset found. Run analysis first.'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def extract_metrics_from_output(output):
    """Extract key metrics from model output"""
    metrics = {
        'best_model': None,
        'test_r2': None,
        'test_rmse': None,
        'test_mae': None,
        'train_r2': None,
        'dataset_size': None
    }

    lines = output.split('\n')
    for i, line in enumerate(lines):
        if 'MEJOR MODELO:' in line:
            # Extract model name and R²
            parts = line.split('MEJOR MODELO:')[1].strip()
            if '(R²' in parts:
                metrics['best_model'] = parts.split('(R²')[0].strip()
                r2_str = parts.split('= ')[1].split(')')[0]
                metrics['test_r2'] = float(r2_str)

        if 'Test R²:' in line:
            try:
                metrics['test_r2'] = float(line.split('Test R²:')[1].split()[0])
            except:
                pass

        if 'Test RMSE:' in line:
            try:
                metrics['test_rmse'] = float(line.split('Test RMSE:')[1].split()[0])
            except:
                pass

        if 'Test MAE:' in line:
            try:
                metrics['test_mae'] = float(line.split('Test MAE:')[1].split()[0])
            except:
                pass

        if 'Dimensiones del dataset:' in line:
            try:
                size_str = line.split('(')[1].split(',')[0]
                metrics['dataset_size'] = int(size_str)
            except:
                pass

    return metrics

def check_generated_images():
    """Check which images were generated"""
    images = []
    image_files = [
        '01_popularity_distribution.png',
        '02_explicit_vs_popularity.png',
        '03_correlation_matrix.png',
        '04_feature_importance.png',
        '05_metrics_evaluation.png',
        '06_predictions_analysis.png'
    ]

    for img in image_files:
        if os.path.exists(img):
            images.append({
                'name': img,
                'title': img.replace('.png', '').replace('_', ' ').title(),
                'path': f'/api/images/{img}'
            })

    return images

if __name__ == '__main__':
    print("="*80)
    print("SPOTIFY POPULARITY ANALYSIS API")
    print("="*80)
    print("\nAPI Running on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  • POST /api/run-analysis - Run ML analysis")
    print("  • GET  /api/status - Get analysis status")
    print("  • GET  /api/results - Get analysis results")
    print("  • GET  /api/images/<name> - Get generated images")
    print("  • GET  /api/dataset-info - Get dataset information")
    print("\n" + "="*80)

    app.run(debug=True, port=5000)
