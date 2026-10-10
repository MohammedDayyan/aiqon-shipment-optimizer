import json
import random
import os

def generate_synthetic_data(num_shipments=30):
    origins = ["Shanghai", "Singapore", "Rotterdam", "Los Angeles", "Hamburg", "Dubai"]
    destinations = ["New York", "London", "Tokyo", "Hamburg", "Sydney", "Mumbai"]
    hubs = [["Busan", "Le Havre"], ["Colombo", "Suez"], ["Rotterdam", "Antwerp"], ["Panama", "Miami"], ["Doha"]]
    profiles = ["time_critical", "budget_optimized", "risk_averse", "balanced"]
    risks = ["Low", "Medium", "High"]

    shipments = []

    for i in range(1,num_shipments+1):

        orig = random.choice(origins)
        dest = random.choice(destinations)
        while orig == dest:
            dest = random.choice(destinations)

        num_routes = random.randint(3,5)
        routes = []

        for r in range(1,num_routes+1):
            cost = round(random.uniform(3000.0,15000.0),2)
            base_time = round(random.uniform(5.0,30.0),1)
            delay_prob = round(random.uniform(0.05,0.45),2)
            delay_dur = round(random.uniform(1.0,5.0),1)
            risk = random.choice(risks)

            routes.append({
                "route_id": f"R{i}-{r}",
                "origin": orig,
                "destination": dest,
                "intermediate_hubs": random.choice(hubs),
                "cost": cost,
                "base_transit_time": base_time,
                "delay_probability": delay_prob,
                "estimated_delay_duration": delay_dur,
                "risk_indicator": risk
            })

        shipments.append({
            "shipment_id": f"SHP-{1000 + i}",
            "cargo_type": random.choice(["General", "Perishable", "High-Value", "Hazardous"]),
            "priority_profile": random.choice(profiles),
            "routes": routes
        })
    
    os.makedirs("data",exist_ok=True)
    with open("data/synthetic_shipments.json","w") as f:
        json.dump(shipments,f,indent=4)
    print(f"Generated {num_shipments} synthetic shipments in data/synthetic_shipments.json[cite: 2]")

if __name__ == "__main__":
    generate_synthetic_data()