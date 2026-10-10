from typing import List
from pydantic import BaseModel, Field

class RouteOption(BaseModel):

    route_id: str
    origin: str
    destination: str
    intermediate_hubs: List[str]
    cost: float = Field(...,gt=0,description="Total financial cost in USD")
    base_transit_time: float = Field(...,gt=0,description="Estimated transit time in days")
    delay_probability: float = Field(...,ge=0.0,le=1.0,description="Probability of delay between 0 and 1")
    estimated_delay_duration: float = Field(...,ge=0,description="Expected delay duration in days if delay occurs")
    risk_indicator: str = Field(...,description="Categorical risk: Low, Medium, High")

class ShipmentRequest(BaseModel):

    shipment_id: str
    cargo_type: str = Field(...,description="General, Perishable, High-Value, Hazardous")
    priority_profile: str = Field("balanced",description="time_critical, budget_optimized, risk_averse, balanced")
    routes : List[RouteOption] = Field(...,nmin_items=2,max_items=5)

class RecommendationResponse(BaseModel):

    shipment_id: str
    recommended_route_id: str
    confidence_score: float
    explanation: str
    evaluated_routes: List[dict]