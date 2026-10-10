def generate_contrastive_explanation(ranked_routes: list,profile: str) -> str:
    """
    Generates a human-readable contrastive explanation comparing Rank 1 vs Rank 2[cite: 2].
    """

    if not ranked_routes:
        return "No routes evaluated."

    best = ranked_routes[0]
    if len(ranked_routes) == 1:
        return f"Route {best['route_id']} is the only available option evaluated under the {profile} profile."

    runner_up = ranked_routes[1]

    cost_diff = best["raw_cost"] - runner_up["raw_cost"]
    time_diff = best["raw_expected_time"] - runner_up["raw_expected_time"]
    risk_diff_val = best["raw_risk"] - runner_up["raw_risk"]
    cost_pct = (abs(cost_diff)/runner_up["raw_cost"]) * 100

    explanation = f"Recommended Route '{best['route_id']}' under the '{profile}' priority profile. "

    if time_diff < 0 and cost_diff > 0:
        explanation += (
            f"While Route '{best['route_id']}' is {cost_pct:.1f}% more expensive (${best['raw_cost']} vs ${runner_up['raw_cost']}), "
            f"it was selected because it reduces expected transit time by {abs(time_diff):.1f} days "
            f"and mitigates disruption risk compared to runner-up '{runner_up['route_id']}'."
        )
    elif cost_diff < 0 and time_diff > 0:
        explanation += (
            f"Route '{best['route_id']}' was selected as the optimal choice because it reduces cost by {cost_pct:.1f}% "
            f"while maintaining acceptable reliability, outperforming '{runner_up['route_id']}' on budget constraints."
        )
    elif risk_diff_val < 0:
        explanation += (
            f"Although alternative '{runner_up['route_id']}' has comparable metrics, Route '{best['route_id']}' was chosen "
            f"due to significantly lower security and geopolitical risk indicators."
        )
    else:
        explanation += (
            f"Route '{best['route_id']}' achieved an optimal trade-off balance score of {best['total_score']}, "
            f"outperforming runner-up '{runner_up['route_id']}' across composite decision criteria."
        )

    return explanation