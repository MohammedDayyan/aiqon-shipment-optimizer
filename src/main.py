import logging
import time
from fastapi import FastAPI, HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
from src.models.schemas import ShipmentRequest, RecommendationResponse
from src.engine.scorer import evaluate_and_rank_routes
from src.engine.explainer import generate_contrastive_explanation
from src.engine.sensitivity import run_sensitivity_analysis

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("aiqon.api")

app = FastAPI(
    title="Aiqon Shipment Route Optimization Engine",
    description="Multi-objective decision support system for global logistics routing under uncertainty[cite: 2].",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time =  time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {duration:.2f}ms")
    return response

@app.get("/")
def root():
    return {"status": "online", "system": "Aiqon Shipment Optimizer API v2.0"}

@app.post("/recommend",response_model = RecommendationResponse)
def recommend_route(payload: ShipmentRequest):

    try:

        ranked_routes = evaluate_and_rank_routes(payload.routes, payload.priority_profile)
        explanation = generate_contrastive_explanation(ranked_routes, payload.priority_profile)
        best_route = ranked_routes[0]

        serialized_routes = [
            {
                "route_id": r["route_id"],
                "cost": r["raw_cost"],
                "expected_transit_time": round(r["raw_expected_time"], 2),
                "risk_indicator": r["route_obj"].risk_indicator,
                "composite_score": r["total_score"]
            }
            for r in ranked_routes
        ]

        confidence = 0.95

        if len(ranked_routes) > 1:
            score_gap = ranked_routes[1]["total_score"] - ranked_routes[0]["total_score"]
            confidence = round(min(0.50 + (score_gap * 2.0), 0.99), 2)

        return RecommendationResponse(
            shipment_id=payload.shipment_id,
            recommended_route_id=best_route["route_id"],
            confidence_score=confidence,
            explanation=explanation,
            evaluated_routes=serialized_routes
        )
    except Exception as e:
        logger.error(f"Error processing shipment {payload.shipment_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sensitivity_analysis")
def sensitivity_endpoint(payload: ShipmentRequest):
    """
    Runs sensitivity analysis by perturbing priority weights to check decision robustness (Improvement 1).
    """

    try:
        analysis = run_sensitivity_analysis(payload.routes,payload.priority_profile)
        return {
            "shipment_id": payload.shipment_id,
            "sensitivity_analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error in sensitivity analysis: {str(e)}")
        raise HTTPException(status_code=400,detail=str(e))