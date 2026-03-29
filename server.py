from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import run_pipeline
import data  # to use default layout for image uploads

app = Flask(__name__)
# Enable CORS so the frontend at port 8000 can communicate with port 5000
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if request.is_json:
            # Handle JSON payload
            req_data = request.get_json()
            if "rooms" not in req_data or "walls" not in req_data:
                return jsonify({"error": "Missing 'rooms' or 'walls' in JSON payload"}), 400
            
            # Run pipeline without rendering 3D view (since it's a server)
            report = run_pipeline(data_dict=req_data, render=False)
            
            return jsonify(report)
            
        elif 'file' in request.files:
            # Handle Image payload (mock OpenCV processing)
            # Future: add OpenCV logic here
            # For now, we simulate parsing and return default data.py values
            
            mock_data = {
                "rooms": data.rooms,
                "walls": data.walls
            }
            
            report = run_pipeline(data_dict=mock_data, render=False)
            return jsonify(report)
            
        else:
            return jsonify({"error": "Unsupported Content-Type"}), 400
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting SANCTUM Backend Server on port 5000...")
    app.run(port=5000, debug=True)
