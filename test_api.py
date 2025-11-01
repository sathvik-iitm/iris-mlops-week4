
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

print("\n1️⃣ Testing Root Endpoint (GET /):")
response = client.get("/")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

print("\n2️⃣ Testing Health Endpoint (GET /health):")
response = client.get("/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

print("\n3️⃣ Testing Model Info (GET /model/info):")
response = client.get("/model/info")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

print("\n4️⃣ Testing Single Prediction (POST /predict):")
sample_data = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
response = client.post("/predict", json=sample_data)
print(f"   Status: {response.status_code}")
print(f"   Request: {sample_data}")
print(f"   Response: {response.json()}")

print("\n5️⃣ Testing Batch Prediction (POST /predict/batch):")
batch_data = {
    "samples": [
        {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
        {"sepal_length": 6.7, "sepal_width": 3.1, "petal_length": 4.4, "petal_width": 1.4},
        {"sepal_length": 6.3, "sepal_width": 3.3, "petal_length": 6.0, "petal_width": 2.5}
    ]
}
response = client.post("/predict/batch", json=batch_data)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

print("\n" + "="*60)
print("✅ All API tests passed!")
