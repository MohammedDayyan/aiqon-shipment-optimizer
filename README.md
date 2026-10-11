# 🚢 Aiqon Intelligent Shipment Route Optimizer

> A decision-support system that recommends a shipment route by balancing cost, expected transit time and risk, and explains *why* that route beat the alternatives.

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-teal.svg)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-cyan.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Built for the **Aiqon AI Internship take-home assignment**: *Optimizing Shipment Routes Under Cost, Time, and Risk Constraints*.


**Deliverables**

| Deliverable | Location |
|---|---|
| Code repository | this repo |
| Technical report (2-3 pages) | [`docs/technical_report.pdf`](docs/technical_report.pdf) |

---

## Table of contents

1. [Problem and what "optimal" means](#1-problem-and-what-optimal-means)
2. [Approach](#2-approach)
3. [Design decisions](#3-design-decisions)
4. [Project structure](#4-project-structure)
5. [Getting started](#5-getting-started)
6. [Example input and output](#6-example-input-and-output)
7. [Synthetic data](#7-synthetic-data)
8. [Assumptions](#8-assumptions)
9. [Evaluation](#9-evaluation)
10. [Limitations](#10-limitations)
11. [Future work](#11-future-work)
12. [Demo](#12-demo)
13. [License](#13-license)

---

## 1. Problem and what "optimal" means

Route selection in global logistics is not "pick the cheapest" or "pick the fastest". A cheaper route may be delayed more often; a faster one may pass through congested or high-risk regions.

Given a shipment with 3-5 candidate routes (each made of multiple legs), this system:

1. **evaluates** every route,
2. **recommends** one based on defined criteria,
3. **explains** why it is preferred over the alternatives.

**Definition of optimal.** The optimal route is the candidate with the **lowest composite penalty** across normalized cost, *expected* transit time and risk. The objective weights depend on the shipment's priority profile (`time_critical`, `budget_optimized`, `risk_averse`, `balanced`). The system is **decision support**: it recommends and explains, and the operator keeps the final say.

---

## 2. Approach

```
[ Shipment request ]
        │
        ▼
┌───────────────────┐
│ Priority profile  │ ──> objective weights (time-critical, budget, risk-averse, balanced)
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ Uncertainty step  │ ──> expected transit time = base + P(delay) × delay duration
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ Min-max normalizer│ ──> cost, time, risk scaled to [0, 1] across the shipment's candidates
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Weighted scorer  │ ──> composite penalty (lower is better), routes ranked
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ Contrastive       │ ──> plain-language explanation: rank 1 vs runner-up
│ explainer         │
└───────────────────┘
```

### Formulas

```
Expected transit time:  E[T] = T_base + P_delay × D_delay

Min-max normalization:  x' = (x − min) / (max − min)     (per shipment, across its candidate routes)

Composite score:        Score = w_cost · cost' + w_time · E[T]' + w_risk · risk'     (lower is better)
```

### Profiles and weights


| Profile | w_cost | w_time | w_risk |
|---|---|---|---|
| `balanced` | 0.35 | 0.35 | 0.30 |
| `time_critical` | 0.15 | 0.55 | 0.30 |
| `budget_optimized` | 0.65 | 0.15 | 0.20 |
| `risk_averse` | 0.15 | 0.25 | 0.60 |

### Risk mapping

Categorical risk (Low / Medium / High) is mapped to numeric penalties before normalization: `TODO: Low = 0.1, Medium = 0.5, High = 0.9`.

---

## 3. Design decisions

| Decision | Why |
|---|---|
| **Weighted scoring, not full multi-objective optimization** | With only 3-5 candidates per shipment, search is trivial. The real requirement is explainability: an operator can see exactly why route A beat route B and which weight change would flip the result. |
| **Expected transit time, not raw time** | A route that is fast on paper but often delayed should not win on its advertised number. Folding delay probability and duration into one value makes reliability comparable with cost. |
| **Min-max normalization** | Cost (currency), time (days) and risk (ordinal) have different scales; normalizing stops the largest unit from dominating the weights. |
| **Priority profiles instead of raw weights** | Operators think "this cargo is urgent", not "w_time = 0.5". Profiles encode context while keeping weights inspectable. |
| **Contrastive explanations** | Operators care about "why this one and not the other?", so the winner is compared with the runner-up instead of described in isolation. |
| **FastAPI + Pydantic v2** | Typed, validated request/response schemas and automatic API docs. |

---

## 4. Project structure

```
aiqon-shipment-optimizer/
├── data/
│   ├── generator.py               # Generates synthetic shipments (3-5 routes each)
│   └── synthetic_shipments.json   # Generated dataset
├── src/
│   ├── main.py                    # FastAPI app and endpoints
│   ├── engine/
│   │   ├── normalizer.py          # Min-max scaling
│   │   ├── profiles.py            # Priority-profile weights
│   │   ├── scorer.py              # Expected time + weighted-sum scoring
│   │   └── explainer.py           # Contrastive explanation logic
│   └── models/
│       └── schemas.py             # Pydantic v2 models
├── tests/
│   └── test_engine.py             # Unit tests: scoring, normalization, explanations
├── frontend/
│   └── index.html                 # Tailwind CSS dashboard
├── docs/
│   └── technical_report.pdf       # 2-3 page report
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 5. Getting started

### Prerequisites

Python 3.11+ (or Docker).

### Option A: local setup

```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate it
#    Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
#    Windows (Command Prompt):
.\.venv\Scripts\activate.bat
#    Linux / macOS:
source .venv/bin/activate
#    Git Bash on Windows:
source .venv/Scripts/activate

# 3. Install dependencies
pip install -r requirements.txt
```

**Start the backend** (terminal 1):

```bash
uvicorn src.main:app --reload --port 8000
```

- API: <http://localhost:8000>
- Swagger docs: <http://localhost:8000/docs>

**Start the frontend** (terminal 2):

```bash
python -m http.server 8080 --directory frontend
```

- Dashboard: <http://localhost:8080>

### Option B: Docker

```bash
docker compose up --build
```


### Regenerate the synthetic dataset

```bash
python data/generator.py
```

Command : python -m data.generator

### Run the tests

```bash
pytest tests/ -v
```

---

## 6. Example input and output

Test /recommend (Multi-Objective Route Recommendation)
Endpoint: POST /recommend

**JSON Input Payload**:

```json
{
  "shipment_id": "SHP-2026-TEST",
  "cargo_type": "Perishable",
  "priority_profile": "time_critical",
  "routes": [
    {
      "route_id": "Route-A",
      "origin": "Singapore",
      "destination": "Hamburg",
      "intermediate_hubs": ["Colombo"],
      "cost": 11500.0,
      "base_transit_time": 9.0,
      "delay_probability": 0.05,
      "estimated_delay_duration": 1.0,
      "risk_indicator": "Low"
    },
    {
      "route_id": "Route-B",
      "origin": "Singapore",
      "destination": "Hamburg",
      "intermediate_hubs": ["Suez"],
      "cost": 7400.0,
      "base_transit_time": 15.0,
      "delay_probability": 0.25,
      "estimated_delay_duration": 3.0,
      "risk_indicator": "Medium"
    },
    {
      "route_id": "Route-C",
      "origin": "Singapore",
      "destination": "Hamburg",
      "intermediate_hubs": ["Cape of Good Hope"],
      "cost": 4900.0,
      "base_transit_time": 24.0,
      "delay_probability": 0.40,
      "estimated_delay_duration": 5.0,
      "risk_indicator": "High"
    }
  ]
}
```

**Response** :

```json
{
  "shipment_id": "SHP-2026-TEST",
  "recommended_route_id": "Route-A",
  "confidence_score": 0.99,
  "explanation": "Recommended Route 'Route-A' under the 'time_critical' priority profile. While Route 'Route-A' is 55.4% more expensive ($11500.0 vs $7400.0), it was selected because it reduces expected transit time by 6.7 days and mitigates disruption risk compared to runner-up 'Route-B'.",
  "evaluated_routes": [
    {
      "route_id": "Route-A",
      "cost": 11500,
      "expected_transit_time": 9.05,
      "risk_indicator": "Low",
      "composite_score": 0.15
    },
    {
      "route_id": "Route-B",
      "cost": 7400,
      "expected_transit_time": 15.75,
      "risk_indicator": "Medium",
      "composite_score": 0.4242
    },
    {
      "route_id": "Route-C",
      "cost": 4900,
      "expected_transit_time": 26,
      "risk_indicator": "High",
      "composite_score": 0.85
    }
  ]
}
```

Test /sensitivity-analysis (Testing Decision Robustness)
Endpoint: POST /sensitivity-analysis

**JSON Input Payload**:
```json
{
  "shipment_id": "SHP-2026-SENSITIVITY",
  "cargo_type": "High-Value",
  "priority_profile": "risk_averse",
  "routes": [
    {
      "route_id": "Route-Alpha",
      "origin": "Shanghai",
      "destination": "New York",
      "intermediate_hubs": ["Panama"],
      "cost": 9800.0,
      "base_transit_time": 12.0,
      "delay_probability": 0.10,
      "estimated_delay_duration": 1.0,
      "risk_indicator": "Low"
    },
    {
      "route_id": "Route-Beta",
      "origin": "Shanghai",
      "destination": "New York",
      "intermediate_hubs": ["Los Angeles"],
      "cost": 6100.0,
      "base_transit_time": 18.0,
      "delay_probability": 0.30,
      "estimated_delay_duration": 3.0,
      "risk_indicator": "Medium"
    }
  ]
}
```

**Response**:
```json
{
  "shipment_id": "SHP-2026-SENSITIVITY",
  "sensitivity_analysis": {
    "is_decision_stable": false,
    "scenarios": [
      {
        "scenario": "Cost-Dominant",
        "applied_weights": {
          "weight_cost": 0.8,
          "weight_time": 0.1,
          "weight_risk": 0.1
        },
        "optimal_route": "Route-Beta",
        "all_scores": [
          {
            "route_id": "Route-Beta",
            "score": 0.2
          },
          {
            "route_id": "Route-Alpha",
            "score": 0.8
          }
        ]
      },
      {
        "scenario": "Time-Dominant",
        "applied_weights": {
          "weight_cost": 0.1,
          "weight_time": 0.8,
          "weight_risk": 0.1
        },
        "optimal_route": "Route-Alpha",
        "all_scores": [
          {
            "route_id": "Route-Alpha",
            "score": 0.1
          },
          {
            "route_id": "Route-Beta",
            "score": 0.9
          }
        ]
      },
      {
        "scenario": "Risk-Dominant",
        "applied_weights": {
          "weight_cost": 0.1,
          "weight_time": 0.1,
          "weight_risk": 0.8
        },
        "optimal_route": "Route-Alpha",
        "all_scores": [
          {
            "route_id": "Route-Alpha",
            "score": 0.1
          },
          {
            "route_id": "Route-Beta",
            "score": 0.9
          }
        ]
      },
      {
        "scenario": "Balanced Equal",
        "applied_weights": {
          "weight_cost": 0.33,
          "weight_time": 0.33,
          "weight_risk": 0.34
        },
        "optimal_route": "Route-Alpha",
        "all_scores": [
          {
            "route_id": "Route-Alpha",
            "score": 0.33
          },
          {
            "route_id": "Route-Beta",
            "score": 0.67
          }
        ]
      }
    ],
    "stability_note": "Decision is sensitive to weight changes near trade-off boundaries."
  }
}
```

Add a dashboard screenshot here: `![Dashboard](docs/Dashboard_1.png)`

---

## 7. Synthetic data

No public dataset has route-level delay distributions, so `data/generator.py` creates synthetic shipments.

- **Size:** `30 shipments`, each with 3-5 candidate routes.
- **Fields per route:** origin, destination, intermediate ports/hubs, cost, base transit time, delay probability, estimated delay duration, risk indicators (e.g. congestion, geopolitical).
- **Trade-off construction:**Global logistics routing requires balancing competing objectives across a dataset of 20 to 50 shipments, with each shipment evaluating 3 to 5 distinct route options. Fundamental economic trade-offs dictate that faster routes incur higher financial costs, whereas cheaper alternatives often compromise reliability by introducing higher delay probabilities and handling bottlenecks.   In addition, paths traversing congested or geopolitically volatile intermediate ports are assigned elevated risk indicators, such as medium or high threat levels. To accurately handle operational uncertainty, our decision framework computes expected transit times by factoring in delay probabilities and potential delay durations across these multi-leg routes.

---

## 8. Assumptions

- Delay probability and delay duration are known point estimates (no uncertainty on the estimates themselves).
- Delays are the only stochastic element; cost and base transit time are deterministic. All costs use one currency.
- Risk categories are ordinal and mapped to numeric penalties.
- Profile weights are hand-set expert judgments, not learned or calibrated.
- Each shipment is optimized in isolation: no capacity limits, no interaction between shipments, no live data.


---



## 9. Limitations

| Limitation | Consequence |
|---|---|
| **Compensatory weighted sum, no hard constraints** | A very cheap route can offset very high risk. There is no way to enforce a deadline, budget cap or restricted region, so an unacceptable route can still rank first. A weighted sum also cannot reach non-convex Pareto-optimal trade-offs. |
| **Per-shipment min-max normalization** | Tiny absolute differences are magnified (a 1% cost gap becomes 0 vs 1). Scores are not comparable across shipments, and adding or removing a route can reorder the others (rank reversal). |
| **Mean-only uncertainty** | Expected time hides variance and tail risk: two routes with the same E[T] can differ greatly in worst-case lateness. Delay is a single number, not a distribution. |
| **Synthetic data only** | Results reflect the generator's assumptions, not real logistics behavior. |

---

## 10. Future work

In priority order:

1. Add **hard constraints** (deadline, budget cap, blocked regions) and filter Pareto-dominated routes before scoring.
2. **Monetize delay** (cost of a day late) so weights have real-world meaning instead of arbitrary values.
3. Run the **Monte Carlo evaluation** against baselines.
4. Add **weight-sensitivity analysis** and a "close call" flag when the top two routes are within a margin.
5. Report **uncertainty-aware metrics** such as P90 transit time or CVaR, and model delay per leg.
6. Validate on real shipment data and calibrate weights from operator decisions.

---

