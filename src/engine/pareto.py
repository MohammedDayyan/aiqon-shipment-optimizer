from typing import List
from src.models.schemas import RouteOption
from src.engine.normalizer import risk_to_numeric

def filter_pareto_optimal_routes(routes: List[RouteOption]) -> List[RouteOption]:
    """
    Filters out strictly dominated routes. A route is dominated if another route
    is better or equal in ALL metrics (cost, expected time, risk) and strictly better in at least one.
    """

    if len(routes) <= 1:
        return routes

    route_metrics = []

    for r in routes:
        exp_time = r.base_transit_time + (r.delay_probability * r.estimated_delay_duration)
        risk_num = risk_to_numeric(r.risk_indicator)
        route_metrics.append({
            "route": r,
            "cost": r.cost,
            "time": exp_time,
            "risk": risk_num
        })

    non_dominated = []
    for i,p in enumerate(route_metrics):
        dominated = False
        for j,q in enumerate(route_metrics):
            if i == j:
                continue
            better_or_equal = (q["cost"] <= p["cost"]) and (q["time"] <= p["time"]) and (q["risk"] <= p["risk"])
            strictly_better = (q["cost"] < p["cost"]) or (q["time"] < p["time"]) or (q["risk"] < p["risk"])

            if better_or_equal and strictly_better:
                dominated = True
                break
        
        if not dominated:
            non_dominated.append(p["route"])
    
    return non_dominated if non_dominated else routes