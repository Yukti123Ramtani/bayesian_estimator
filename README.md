# 📦 Bayesian Inventory Risk Estimator & Power BI Analytics Dashboard

An end-to-end Machine Learning Engineering & Business Intelligence system that quantifies inventory reorder uncertainty and stock discrepancy risks. This repository bridges statistical data engineering (**Beta-Binomial conjugacy**), a live production microservice (**FastAPI on Render**), and an interactive 5-page executive BI dashboard (**Power BI**).

---

## 📌 System Architecture & Pipeline

```text
[ Multi-Source Datasets ]
  ├── order_products__train.csv (1.38M+ orders)
  ├── products.csv / products_2.csv
  ├── aisles.csv
  └── departments.csv
            │
            ▼
[ Feature Engineering Pipeline (Pandas / SciPy) ]
  ├── Aisle-level empirical priors (α_prior, β_prior)
  ├── Conjugacy updates (post_alpha, post_beta)
  └── 95% Credible Intervals → `product_reorder_posterior.csv` (49,593 items)
            │
            ├─────────────────────────────────────────────┐
            ▼                                             ▼
[ Live FastAPI Service (Render) ]              [ Power BI Dashboard (.pbix) ]
  ├── POST `/estimate/stock-confidence`          ├── 01 Executive Overview
  ├── Dynamic 95% High-Density Intervals (HDI)   ├── 02 Bayesian Reorder Analysis


💡 Key Features

Statistical Rigor over Point Estimates: Replaces naive point reorder rates with Beta-Binomial Bayesian posterior updating. Low-sample items are pulled smoothly toward aisle-level empirical priors, preventing rare single-order spikes from causing false inventory alarms.

Pre-Calculated Feature Store: Consolidated 1.38M+ transactional orders into a unified analytical feature dataset (product_reorder_posterior.csv) containing posterior parameters ($\alpha, \beta$), raw vs. posterior means, and exact 95% Credible Interval widths (ci_width).

Production API Service: Deployed a containerized Python/FastAPI backend on Render that calculates real-time High-Density Intervals (HDI) and risk categories from incoming inspection payloads.

Dynamic BI Integration: Connected Power BI to the live Render microservice using custom M-code (Web.Contents), enabling parameterized HTTP POST requests to dynamically update report gauge visuals and risk KPI cards.


🛠️ Tech Stack
Language: Python 3.10+

Backend & API: FastAPI, Uvicorn, Pydantic

Data Processing & Analytics: Pandas, NumPy, SciPy

Business Intelligence: Power BI Desktop, M-Code / Power Query

Deployment & Hosting: Render, GitHub


📊 Dashboard Structure
The Power BI report (bayesian_estimator.pbix) consists of 5 specialized pages:

01 Executive Overview: High-level volume trends, departmental order distributions, and core KPI tracking.

02 Bayesian Reorder Analysis: Visualizing shrinkage effects, uncertainty spreads (ci_width), and posterior distributions against raw rates.

03 Product Reorder Audit: Searchable product-level audit grid with cross-filtering reactivity across aisles and departments.

04 Strategic Insights: Business recommendations for inventory prioritization, safety stock buffers, and promotional strategy.

05 Real-Time Inventory API: Parameterized inspection interface connected to the live Render endpoint displaying dynamic 95% HDI gauge bounds and risk classifications.



🚀 Live API Reference
Method: POST

URL: https://bayesian-estimator-mhpy.onrender.com/estimate/stock-confidence

Interactive Docs (Swagger): https://bayesian-estimator-mhpy.onrender.com/docs

Example Request Body Payload
{
  "prior_alpha": 2.0,
  "prior_beta": 8.0,
  "picking_attempts": 100,
  "reported_discrepancies": 12
}

Example JSON Response Payload
{
  "posterior_alpha": 14.0,
  "posterior_beta": 96.0,
  "posterior_mean": 0.1273,
  "hdi_95_lower": 0.0720,
  "hdi_95_upper": 0.1953,
  "stock_risk_category": "MODERATE_MISCOUNT_RISK"
}

💻 Local Setup & Installation

1. Clone the Repository
Bash
git clone [https://github.com/your-username/bayesian-inventory-risk-engine.git](https://github.com/your-username/bayesian-inventory-risk-engine.git)
cd bayesian-inventory-risk-engine

2. Set Up Virtual Environment & Install Requirements
Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

3. Run FastAPI Server Locally
Bash
uvicorn main:app --reload
Navigate to http://127.0.0.1:8000/docs in your browser to inspect and test the endpoint interactively.

4. Open Dashboard
Open bayesian_estimator.pbix in Power BI Desktop. Ensure active internet connectivity to perform live data refreshes against the Render backend endpoint.
  └── Automated Risk Categorization              ├── 03 Product Reorder Audit
            │                                    ├── 04 Strategic Insights
            └──────────► [ M-Code Integration ] ─► └── 05 Real-Time Inventory API
