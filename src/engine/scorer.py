import logging
from typing import List
from src.models.schemas import RouteOption
from src.engine.normalizer import normalize_routes
from src.engine.profiles import get_profile_weights
from src.engine.pareto import filter_pareto_optimal_routes

def evaluate_and_rank_routes(routes: List[RouteOption], priority_profile: str) -> List[dict]:
    """
    Scores and ranks routes using Pareto filtering, uncertainty adjustment, and weighted penalty models.
    """
    logger.info(f"Evaluating {len(routes)} raw routes under profile '{priority_profile}'")    

    filtered_routes = filter_pareto_optimal_routes(routes)
    logger.info(f"Pareto filtering retained {len(filtered_routes)} out of {len(routes)} routes.")
    weights = get_profile_weights(priority_profile)
    norm_data = normalize_routes(filtered_routes)

    scored_routes = []
    for item in norm_data:

        total_score = (
            weights["weight_cost"] * item["norm_cost"] +
            weights["weight_time"] * item["norm_time"] +
            weights["weight_risk"] * item["norm_risk"]
        )

        item["total_score"] = round(total_score, 4)
        scored_routes.append(item)
    
    scored_routes.sort(key=lambda x:x["total_score"])
    logger.info(f"Top recommended route: {scored_routes[0]['route_id']} with score {scored_routes[0]['total_score']}")

    return scored_routes