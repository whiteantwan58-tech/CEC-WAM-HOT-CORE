"""
api_server.py
-------------

Flask API server to serve chart data and automation status for the CEC-WAM live system.
Provides endpoints for index.html to fetch dynamic chart data.

Usage:
    python api_server.py
"""

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'service': 'CEC-WAM Chart API'
    })


@app.route('/api/chart-data', methods=['GET'])
def get_chart_data():
    """Get chart data for visualization"""
    try:
        chart_data_file = os.path.join(DATA_DIR, 'chart_data.json')
        
        if not os.path.exists(chart_data_file):
            return jsonify({
                'error': 'Chart data not found',
                'message': 'Run chart_automation.py first'
            }), 404
        
        with open(chart_data_file, 'r') as f:
            data = json.load(f)
        
        return jsonify(data)
    
    except Exception as e:
        logger.error(f"Error loading chart data: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/automation-status', methods=['GET'])
def get_automation_status():
    """Get automation status report"""
    try:
        report_file = os.path.join(DATA_DIR, 'automation_report.json')
        
        if not os.path.exists(report_file):
            return jsonify({
                'error': 'Automation report not found',
                'message': 'Run chart_automation.py first'
            }), 404
        
        with open(report_file, 'r') as f:
            data = json.load(f)
        
        return jsonify(data)
    
    except Exception as e:
        logger.error(f"Error loading automation status: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    """List all available datasets"""
    try:
        datasets = []
        
        # CSV files in root
        for file in os.listdir(BASE_DIR):
            if file.endswith('.csv'):
                datasets.append({
                    'name': file,
                    'path': file,
                    'type': 'csv'
                })
        
        # CSV files in data directory
        if os.path.exists(DATA_DIR):
            for file in os.listdir(DATA_DIR):
                if file.endswith('.csv'):
                    datasets.append({
                        'name': file,
                        'path': f'data/{file}',
                        'type': 'csv'
                    })
        
        return jsonify({
            'count': len(datasets),
            'datasets': datasets
        })
    
    except Exception as e:
        logger.error(f"Error listing datasets: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/run-automation', methods=['POST'])
def run_automation():
    """Trigger the automation script"""
    try:
        import subprocess
        
        # Run the automation script
        result = subprocess.run(
            ['python', 'chart_automation.py'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Automation completed successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Automation failed',
                'error': result.stderr
            }), 500
    
    except Exception as e:
        logger.error(f"Error running automation: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/live-data', methods=['GET'])
def get_live_data():
    """Get live aggregated data for dashboard"""
    try:
        live_data = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {}
        }
        
        # Load pump.fun data
        pump_file = os.path.join(BASE_DIR, 'pump.fun.csv')
        if os.path.exists(pump_file):
            import pandas as pd
            df = pd.read_csv(pump_file)
            live_data['metrics']['pump_fun'] = {
                'total_transactions': len(df),
                'total_value': df['Value'].sum() if 'Value' in df.columns else 0,
                'latest_transaction': df.iloc[-1].to_dict() if len(df) > 0 else None
            }
        
        # Load BlackHoles data
        blackholes_file = os.path.join(BASE_DIR, 'BlackHoles.csv')
        if os.path.exists(blackholes_file):
            import pandas as pd
            df = pd.read_csv(blackholes_file)
            live_data['metrics']['blackholes'] = {
                'total_discoveries': len(df),
                'status_distribution': df['STATUS'].value_counts().to_dict() if 'STATUS' in df.columns else {}
            }
        
        # Load CEC Matrix data
        cec_file = os.path.join(BASE_DIR, 'CEC Matrix System Operational Metrics and Assets - FINANCE_HUB (1).csv')
        if os.path.exists(cec_file):
            import pandas as pd
            df = pd.read_csv(cec_file)
            live_data['metrics']['cec_assets'] = {
                'total_assets': len(df),
                'asset_classes': df['A (ASSET CLASS)'].tolist() if 'A (ASSET CLASS)' in df.columns else []
            }
        
        return jsonify(live_data)
    
    except Exception as e:
        logger.error(f"Error getting live data: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting CEC-WAM Chart API Server...")
    logger.info(f"Base directory: {BASE_DIR}")
    logger.info(f"Data directory: {DATA_DIR}")
    
    # Check if data directory exists
    if not os.path.exists(DATA_DIR):
        logger.warning(f"Data directory not found: {DATA_DIR}")
        os.makedirs(DATA_DIR, exist_ok=True)
    
    # Use debug mode only in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
