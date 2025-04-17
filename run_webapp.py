import requests

receipt = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },
        { "shortDescription": "Emils Cheese Pizza", "price": "12.25" },
        { "shortDescription": "Knorr Creamy Chicken", "price": "1.26" },
        { "shortDescription": "Doritos Nacho Cheese", "price": "3.35" },
        { "shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00" }
    ],
    "total": "35.35"
}

"""
Endpoint: Process Receipts
"""
res = requests.post("http://127.0.0.1:8000/receipts/process", json=receipt)
print("POST Response:", res.json())

"""
Endpoint: Get Points
"""
receipt_id = res.json().get("id")
points_res = requests.get(f"http://127.0.0.1:8000/receipts/{receipt_id}/points")
print("GET Response:", points_res.json())
