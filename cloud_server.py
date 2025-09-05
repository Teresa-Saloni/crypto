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
HE.contextGen(p=65537)  # Plaintext modulus
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
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"status": "success", "filename": file.filename})

@app.route("/train", methods=["POST"])
def train_model():
    data = []
    for fname in os.listdir(UPLOAD_FOLDER):
        with open(os.path.join(UPLOAD_FOLDER, fname), "r") as f:
            for line in f:
                try:
                    val = float(line.strip())
                    enc_val = HE.encryptFrac(val)
                    data.append(enc_val)
                except:
                    continue
    # Save encrypted data
    joblib.dump(data, "encrypted_data.pkl")
    return jsonify({"status": "success", "message": "Training started on encrypted data 🚀"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
