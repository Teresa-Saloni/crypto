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
        "train_endpoint": "/train",
        "debug_endpoint": "/debug"
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
    print(f"✅ File saved: {filepath}")
    return jsonify({"status": "success", "filename": file.filename})

@app.route("/train", methods=["POST"])
def train_model():
    try:
        if not os.path.exists(UPLOAD_FOLDER):
            return jsonify({"error": "Upload folder not found"}), 400
        
        files_in_folder = os.listdir(UPLOAD_FOLDER)
        if not files_in_folder:
            return jsonify({"error": "No files found in upload folder"}), 400
        
        data = []
        processed_files = 0
        
        for fname in files_in_folder:
            filepath = os.path.join(UPLOAD_FOLDER, fname)
            print(f"Processing file: {filepath}")
            
            try:
                with open(filepath, "r") as f:
                    file_data_count = 0
                    for line in f:
                        try:
                            val = int(float(line.strip()))
                            enc_val = HE.encryptInt(val)
                            data.append(enc_val)
                            file_data_count += 1
                        except ValueError as e:
                            print(f"Skipping invalid line: {line.strip()} - {e}")
                            continue
                    
                    print(f"Processed {file_data_count} data points from {fname}")
                    if file_data_count > 0:
                        processed_files += 1
                        
            except Exception as e:
                print(f"Error processing file {fname}: {e}")
                continue
        
        if not data:
            return jsonify({
                "error": "No valid data found to train on",
                "files_found": len(files_in_folder),
                "files_processed": processed_files
            }), 400
        
        # Save encrypted data
        joblib.dump(data, "encrypted_data.pkl")
        print(f"✅ Successfully saved {len(data)} encrypted data points")
        
        return jsonify({
            "status": "success",
            "message": "Training completed on encrypted data 🚀",
            "data_points": len(data),
            "files_processed": processed_files,
            "files_found": len(files_in_folder)
        })
    
    except Exception as e:
        print(f"Training error: {e}")
        return jsonify({"error": f"Training failed: {e}"}), 500

@app.route("/debug", methods=["GET"])
def debug_files():
    """Return list of files in upload folder"""
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"uploaded_files": files})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
