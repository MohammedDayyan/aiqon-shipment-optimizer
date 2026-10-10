from typing import List
from src.models.schemas import RouteOption
from src.engine.normalizer import normalize_routes

def run_sensitivity_analysis(routes: List[RouteOption], base_profile: str)->dict:
    """
    Perturbs priority weights across cost, time, and risk to determine 
    how sensitive the final route recommendation is to weight shifts.
    """

    perbutations = [
        {"name": "Cost-Dominant", "weights": {"weight_cost": 0.80, "weight_time": 0.10, "weight_risk": 0.10}},
        {"name": "Time-Dominant", "weights": {"weight_cost": 0.10, "weight_time": 0.80, "weight_risk": 0.10}},
        {"name": "Risk-Dominant", "weights": {"weight_cost": 0.10, "weight_time": 0.10, "weight_risk": 0.80}},
        {"name": "Balanced Equal", "weights": {"weight_cost": 0.33, "weight_time": 0.33, "weight_risk": 0.34}}
    ]

    sensitivity_results = []
    for p in perbutations:
        norm_data = normalize_routes(routes)
        w = p["weights"]

        scored = []
        for item in norm_data:
            score = w["weight_cost"] * item["norm_cost"] + w["weight_time"] * item["norm_time"] + w["weight_risk"] * item["norm_risk"]
            scored.append({"route_id": item["route_id"], "score": round(score, 4)})
        
        scored.sort(key=lambda x: x["score"])
        best_route = scored[0]["route_id"] if scored else None
        
        sensitivity_results.append({
            "scenario": p["name"],
            "applied_weights": w,
            "optimal_route": best_route,
            "all_scores": scored
        })

    recommended_routes = [res["optimal_route"] for res in sensitivity_results]
    is_stable = len(set(recommended_routes)) == 1

    return {
        "is_decision_stable": is_stable,
        "scenarios": sensitivity_results,
        "stability_note": "Decision is robust across weight shifts." if is_stable else "Decision is sensitive to weight changes near trade-off boundaries."
    }