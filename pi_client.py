# pi_client.py - Raspberry Pi Client for Homomorphic Encryption
import requests
import random
import time

CLOUD_URL = "https://crypto-hedy.onrender.com"

def generate_sensor_data():
    print("📡 Generating sensor data...")
    data = []
    for i in range(10):
        temp = round(random.uniform(20.0, 35.0), 2)
        data.append(temp)
        time.sleep(0.1)
    
    with open("sensor_data.txt", "w") as f:
        for temp in data:
            f.write(f"{int(temp)}\n")  # integers only
    
    print(f"✅ Generated {len(data)} sensor readings")
    return "sensor_data.txt"

def upload_to_cloud(filename):
    print(f"☁️ Uploading {filename} to cloud...")
    try:
        with open(filename, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{CLOUD_URL}/upload", files=files, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful: {result}")
            return result
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def check_debug():
    """Optional: Check uploaded files on server"""
    try:
        response = requests.get(f"{CLOUD_URL}/debug", timeout=10)
        print(f"Debug Status: {response.status_code}")
        print(f"Debug Response: {response.json()}")
    except Exception as e:
        print(f"❌ Debug error: {e}")

def train_on_cloud():
    print("🧠 Starting training on encrypted data...")
    try:
        response = requests.post(f"{CLOUD_URL}/train", timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Training successful: {result}")
            return result
        else:
            print(f"❌ Training failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Training error: {e}")
        return None

def main():
    print("🌩️ Connecting Raspberry Pi to Cloud...")
    print(f"🔗 Cloud URL: {CLOUD_URL}")

    # Test connection
    try:
        response = requests.get(CLOUD_URL, timeout=10)
        print(f"✅ Cloud connection successful!")
        print(f"📋 Server info: {response.json()}")
    except Exception as e:
        print(f"❌ Cannot connect to cloud: {e}")
        return

    # Step 1: Generate sensor data
    filename = generate_sensor_data()

    # Step 2: Upload to cloud
    upload_result = upload_to_cloud(filename)
    if not upload_result:
        return

    # Step 3: Check uploaded files (optional)
    check_debug()

    # Step 4: Train on encrypted data
    train_result = train_on_cloud()
    if not train_result:
        return

    print("\n🎉 SUCCESS! Homomorphic Encryption Pipeline Complete!")
    print("📊 Summary:")
    print(f"   📤 Upload Response: {upload_result}")
    print(f"   🧠 Train Response: {train_result}")

if __name__ == "__main__":
    main()
