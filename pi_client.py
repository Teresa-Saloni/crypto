# pi_client.py - Raspberry Pi Client for Homomorphic Encryption
import requests
import json
import random
import time

# 🔥 YOUR ACTUAL RENDER URL
CLOUD_URL = "https://crypto-hedy.onrender.com"

def generate_sensor_data():
    """Simulate Raspberry Pi sensor data"""
    print("📡 Generating sensor data...")
    data = []
    for i in range(10):
        # Simulate temperature readings (20-35°C)
        temp = round(random.uniform(20.0, 35.0), 2)
        data.append(temp)
        time.sleep(0.1)  # Simulate sensor reading delay
    
    # Save to file (convert to integers for BFV scheme)
    with open("sensor_data.txt", "w") as f:
        for temp in data:
            f.write(f"{int(temp)}\n")  # Convert to integer!
    
    print(f"✅ Generated {len(data)} sensor readings")
    return "sensor_data.txt"

def upload_to_cloud(filename):
    """Upload encrypted data to cloud"""
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
            print(f"❌ Upload failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return None

def train_on_cloud():
    """Trigger training on encrypted data"""
    print("🧠 Starting training on encrypted data...")
    
    try:
        response = requests.post(f"{CLOUD_URL}/train", timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Training successful: {result}")
            return result
        else:
            print(f"❌ Training failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Training error: {str(e)}")
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
        print(f"❌ Cannot connect to cloud: {str(e)}")
        return
    
    # Step 1: Generate sensor data
    filename = generate_sensor_data()
    
    # Step 2: Upload to cloud
    upload_result = upload_to_cloud(filename)
    if not upload_result:
        return
    
    # Step 3: Train on encrypted data
    train_result = train_on_cloud()
    if not train_result:
        return
    
    print("\n🎉 SUCCESS! Homomorphic Encryption Pipeline Complete!")
    print("📊 Summary:")
    print(f"   📤 Upload Response: {upload_result}")
    print(f"   🧠 Train Response: {train_result}")

if __name__ == "__main__":
    main()
