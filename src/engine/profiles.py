def get_profile_weights(profile_name: str)->dict:
    """
    Returns weights for cost, expected time, and risk based on priority profile.
    Weights sum to 1.0.
    """

    profiles = {
        "time_critical":{
            "weight_cost": 0.15,
            "weight_time": 0.55,
            "weight_risk": 0.30
        },
        "budget_optimized":{
            "weight_cost": 0.65,
            "weight_time": 0.15,
            "weight_risk": 0.20
        },
        "risk_averse":{
            "weight_cost": 0.15,
            "weight_time": 0.25,
            "weight_risk": 0.60
        },
        "balanced":{
            "weight_cost": 0.35,
            "weight_time": 0.35,
            "weight_risk": 0.30
        }
    }

    return profiles.get(profile_name,profiles["balanced"])