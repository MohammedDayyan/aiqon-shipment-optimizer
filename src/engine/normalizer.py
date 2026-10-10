from typing import List
from src.models.schemas import RouteOption

def risk_to_numeric(risk: str)-> float:

    mapping = {"low": 0.1,"medium": 0.5,"high": 0.9}

    return mapping.get(risk.lower(),0.5)

def normalize_routes(routes: List[RouteOption]) -> List[dict]:

    costs = [r.cost for r in routes]

    expected_times = [r.base_transit_time + (r.delay_probability * r.estimated_delay_duration) for r in routes]

    risks = [risk_to_numeric(r.risk_indicator) for r in routes]

    min_cost, max_cost = min(costs), max(costs)
    min_time, max_time = min(expected_times), max(expected_times)
    min_risk, max_risk = min(risks), max(risks)

    normalized_data = []

    for i,route in enumerate(routes):

        norm_cost = (costs[i] - min_cost)/(max_cost - min_cost) if max_cost != min_cost else 0.0
        norm_time = (expected_times[i] - min_time)/(max_time - min_time) if max_time != min_time else 0.0
        norm_risk = (risks[i] - min_risk)/(max_risk - min_risk) if max_risk != min_risk else 0.0

        normalized_data.append({
            "route_id": route.route_id,
            "route_obj": route,
            "raw_cost": costs[i],
            "raw_expected_time": expected_times[i],
            "raw_risk": risks[i],
            "norm_cost": norm_cost,
            "norm_time": norm_time,
            "norm_risk": norm_risk
        })

    return normalized_data