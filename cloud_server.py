# cloud_server.py
import os
from flask import Flask, request, jsonify
from Pyfhel import Pyfhel
import joblib

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Homomorphic Encryption context
HE = Pyfhel()
HE.contextGen(scheme='bfv', n=4096, t_bits=20, sec=128)  # BFV scheme with proper parameters
HE.keyGen()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Cloud HE Server running 🚀",
        "upload_endpoint": "/upload",
        "train_endpoint": "/train"
    })

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"status": "success", "filename": file.filename})

@app.route("/train", methods=["POST"])
def train_model():
    try:
        data = []
        for fname in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, fname)
            with open(filepath, "r") as f:
                for line in f:
                    try:
                        val = int(float(line.strip()))  # Convert to int for BFV scheme
                        enc_val = HE.encryptInt(val)  # Use encryptInt for BFV
                        data.append(enc_val)
                    except:
                        continue
        
        if not data:
            return jsonify({"error": "No valid data found to train on"}), 400
        
        # Save encrypted data
        joblib.dump(data, "encrypted_data.pkl")
        return jsonify({
            "status": "success", 
            "message": "Training started on encrypted data 🚀",
            "data_points": len(data)
        })
    
    except Exception as e:
        return jsonify({"error": f"Training failed: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
