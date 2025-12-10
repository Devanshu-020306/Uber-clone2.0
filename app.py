from flask import Flask, jsonify
from flask_cors import CORS
import random
import math
import time

app = Flask(__name__)
CORS(app)

# 1. SETUP DRIVERS
def generate_drivers():
    drivers = []
    # Starting around Mumbai (matches your screenshot location)
    base_lat = 19.0760
    base_lon = 72.8777
    
    for i in range(15):
        drivers.append({
            "id": i,
            "lat": base_lat + random.uniform(-0.03, 0.03),
            "lon": base_lon + random.uniform(-0.03, 0.03),
            "car": random.choice(["Uber Go", "Uber Premier", "Uber XL"]),
            "angle": random.uniform(0, 360), # Direction they are facing
            "speed": 0.00004 # Movement speed
        })
    return drivers

current_drivers = generate_drivers()

@app.route('/drivers', methods=['GET'])
def get_drivers():
    # 2. MOVE DRIVERS SMOOTHLY
    for driver in current_drivers:
        # Convert angle to radians for movement math
        rad = math.radians(driver["angle"])
        
        # Move X and Y based on angle
        driver["lat"] += driver["speed"] * math.cos(rad) * 10 
        driver["lon"] += driver["speed"] * math.sin(rad) * 10
        
        # 5% chance to turn slightly (so they don't drive in straight lines forever)
        if random.random() < 0.05:
            driver["angle"] += random.uniform(-20, 20)

    return jsonify(current_drivers)

@app.route('/calculate_fare', methods=['POST'])
def calculate_fare():
    # Fake fare logic for the "Search" button
    dist = round(random.uniform(2.5, 12.0), 1)
    return jsonify({
        "distance": f"{dist} km",
        "options": [
            {"type": "Uber Go", "price": int(dist * 12 + 40), "time": "4 min"},
            {"type": "Premier", "price": int(dist * 18 + 50), "time": "6 min"},
            {"type": "Uber XL", "price": int(dist * 22 + 80), "time": "9 min"}
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)