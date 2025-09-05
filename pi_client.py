# pi_client.py
import requests

CLOUD_URL = "https://your-render-url.onrender.com"  # Replace with your Render URL

def upload_file():
    try:
        with open("sensor_data.txt", "rb") as f:
            files = {"file": f}
            response = requests.post(f"{CLOUD_URL}/upload", files=files)
        print("Upload Response:", response.json())
    except Exception as e:
        print("Upload failed:", e)

def train_model():
    try:
        response = requests.post(f"{CLOUD_URL}/train")
        print("Train Response:", response.json())
    except Exception as e:
        print("Training failed:", e)

if __name__ == "__main__":
    print("🌩️ Connecting Raspberry Pi to Cloud...")
    upload_file()
    train_model()
