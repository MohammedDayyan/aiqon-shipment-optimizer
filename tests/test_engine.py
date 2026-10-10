from src.models.schemas import RouteOption
from src.engine.scorer import evaluate_and_rank_routes
from src.engine.explainer import generate_contrastive_explanation

def test_scoring_and_ranking():
    r1 = RouteOption(
        route_id="R1", origin="A", destination="B", intermediate_hubs=["H1"],
        cost=5000.0, base_transit_time=10.0, delay_probability=0.1, estimated_delay_duration=1.0, risk_indicator="Low"
    )
    r2 = RouteOption(
        route_id="R2", origin="A", destination="B", intermediate_hubs=["H2"],
        cost=3000.0, base_transit_time=25.0, delay_probability=0.5, estimated_delay_duration=4.0, risk_indicator="High"
    )
    ranked = evaluate_and_rank_routes([r1, r2], "time_critical")
    assert ranked[0]["route_id"] == "R1"

def test_explanation_generation():
    r1 = RouteOption(
        route_id="R1", origin="A", destination="B", intermediate_hubs=["H1"],
        cost=5000.0, base_transit_time=10.0, delay_probability=0.1, estimated_delay_duration=1.0, risk_indicator="Low"
    )
    r2 = RouteOption(
        route_id="R2", origin="A", destination="B", intermediate_hubs=["H2"],
        cost=3000.0, base_transit_time=20.0, delay_probability=0.2, estimated_delay_duration=2.0, risk_indicator="Medium"
    )
    ranked = evaluate_and_rank_routes([r1, r2], "balanced")
    explanation = generate_contrastive_explanation(ranked, "balanced")
    assert isinstance(explanation, str)
    assert "Route" in explanation