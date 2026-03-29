"""
Flask API Server for SANCTUM
"""

import json
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import run_pipeline

app = Flask(__name__)
CORS(app)


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze floor plan - handles both image and JSON input."""
    
    content_type = request.content_type or ""
    
    # Case 1: Image upload (FormData)
    if "multipart/form-data" in content_type:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400
        
        # Save to temp file and run pipeline
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            result = run_pipeline(input_path=tmp_path, render=False)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Case 2: JSON input
    elif "application/json" in content_type:
        try:
            data = request.get_json()
            
            # Validate required keys
            if 'rooms' not in data or 'walls' not in data:
                return jsonify({
                    "error": "JSON must contain 'rooms' and 'walls' keys"
                }), 400
            
            # Write to temp file for pipeline
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
                json.dump(data, tmp)
                tmp_path = tmp.name
            
            try:
                result = run_pipeline(input_path=tmp_path, render=False)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
                
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON"}), 400
    
    # Unsupported content type
    return jsonify({
        "error": "Content-Type must be multipart/form-data or application/json"
    }), 400


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
