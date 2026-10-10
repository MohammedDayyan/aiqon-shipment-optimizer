# 🚢 Aiqon Intelligent Shipment Route Optimizer

> **A Decision Support System for Multi-Objective Logistics Routing Under Uncertainty**[cite: 1, 2]

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-teal.svg)](https://fastapi.tiangolo.com/)
[![Docker Compose](https://img.shields.io/badge/Docker-Compose-cyan.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Overview

In global logistics, route selection involves complex trade-offs between financial cost, estimated transit time, reliability, and geopolitical risk[cite: 1]. This project implements an intelligent decision-support backend and interactive web interface designed for **Aiqon**, optimizing shipment routes by balancing competing objectives under uncertainty.

Rather than relying on brittle static formulas or optimizing for a single metric, the system uses a **Context-Aware Multi-Objective Decision Framework** equipped with uncertainty modeling and contrastive explainability.

---

## 🏗️ System Architecture & Design Logic

```text
[ Shipment Request / Payload ]
             │
             ▼
┌───────────────────┐
│ Priority Profile  │ ──> Dynamic Weights (Time-Critical, Budget, Risk-Averse)
└───────────────────┘
             │
             ▼
┌───────────────────┐
│Uncertainty Engine │ ──> Expected Transit Time = Base Time + (Delay Prob × Delay Dur)
└───────────────────┘
             │
             ▼
┌───────────────────┐
│Min-Max Normalizer │ ──> Scales Cost, Time, & Risk to [0, 1] Normalized Penalty Space
└───────────────────┘
             │
             ▼
┌───────────────────┐
│  Weighted Scorer  │ ──> Calculates Composite Penalty Score & Ranks Routes
└───────────────────┘
             │
             ▼
┌───────────────────┐
│Contrastive Engine │ ──> Generates Human-Readable Explanation (Rank 1 vs. Runner-Up)
└───────────────────┘
```

### Key Technical Pillars
1. **Uncertainty Adjustment**: Instead of using raw transit estimates, the system models delay risk by calculating **Expected Transit Time**:
   $$\text{Expected Time} = \text{Base Transit Time} + (\text{Delay Probability} \times \text{Estimated Delay Duration})$$2. **Min-Max Normalization**: Scales financial figures ($$), transit days, and categorical risks (Low/Med/High mapped to numerical penalties) into a standardized $[0, 1]$ range to prevent scale distortion.
3. **Dynamic Priority Profiling**: Automatically weights objectives based on cargo context (`time_critical`, `budget_optimized`, `risk_averse`, or `balanced`)[cite: 2].
4. **Contrastive Explainability**: Automatically contrasts the winning route against the runner-up to explain precisely *why* a route was selected (e.g., justifying a 15% cost increase due to a 40% reduction in delay risk)[cite: 2].

---

## 📁 Project Structure

```text
aiqon-shipment-optimizer/
├── data/
│   ├── generator.py               # Generates synthetic shipments with 3-5 routes each[cite: 2]
│   └── synthetic_shipments.json   # Generated raw logistics dataset
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application and routing endpoints
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── normalizer.py          # Min-Max scaling logic
│   │   ├── profiles.py            # Priority profile weight mappings
│   │   ├── scorer.py              # Expected value & multi-objective weighted sum scoring
│   │   └── explainer.py           # Contrastive explanation heuristics
│   └── models/
│       ├── __init__.py
│       └── schemas.py             # Pydantic v2 data validation models
├── tests/
│   ├── __init__.py
│   └── test_engine.py             # Unit tests for scoring, normalization, and explainability
├── frontend/
│   └── index.html                 # Lightweight Tailwind CSS interactive web dashboard
├── docs/
│   └── technical_report.pdf       # 2-3 page design document covering approach and limitations[cite: 3]
├── Dockerfile                     # Container configuration for backend services
├── docker-compose.yml             # Orchestration for API service
├── requirements.txt               # Locked project dependencies
└── README.md
```
---

### Commands To execute:
  1.**Activate virtual environment**:
           ----- python -m venv .venv
           In Powershell:    .\.venv\Scripts\Activate.ps1
           In Command Prompt:     .\.venv\Scripts\activate.bat
           In Git Bash:     source .venv/Scripts/activate
  2.**Install all required libraries**:
           ---- pip install -r requirements.txt
  3.**Backend**:
           ---- uvicorn src.main:app --reload --port 8000
  4.**Frontend**:
           ---- python -m http.server 8080 --directory frontend   
