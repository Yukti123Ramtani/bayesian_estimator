📦 End-to-End Bayesian Risk Estimation Engine & Executive BI DashboardAn end-to-end Machine Learning Engineering & Analytics system that quantifies inventory reorder uncertainty and discrepancy risks. This repository bridges statistical data engineering (Beta-Binomial conjugacy), a live production microservice (FastAPI on Render), and an interactive 5-page executive BI dashboard (Power BI).📌 Architecture Overview[ Raw Relational Files ] 
  ├── order_products__train.csv (1.38M+ rows)
  ├── products.csv / products_2.csv
  ├── aisles.csv
  └── departments.csv
            │
            ▼
[ Offline Feature Pipeline (Pandas / SciPy) ]
  ├── Empirical Aisle-Level Priors (α_prior, β_prior)
  ├── Conjugacy Updates & 95% Credible Intervals (CI)
  └── Generates `product_reorder_posterior.csv` (49,593 items)
            │
            ├─────────────────────────────────────────┐
            ▼                                         ▼
[ Live FastAPI Backend (Render) ]          [ Power BI Desktop Dashboard ]
  ├── POST `/estimate/stock-confidence`      ├── 01 Executive Overview
  ├── Parameterized Inspection Requests       ├── 02 Bayesian Reorder Analysis
  └── Real-Time 95% HDI Bounds Calculation   ├── 03 Product Reorder Audit
            │                                ├── 04 Strategic Insights
            └────► [ M-Code Web.Contents ] ──► └── 05 Real-Time Inventory API
💡 Key FeaturesStatistical Rigor over Point Estimates: Replaces naive point reorder rates with Beta-Binomial Bayesian posterior updating. Low-sample items are pulled smoothly toward aisle-level empirical priors, preventing false risk alarms from rare single-order spikes.Scalable Feature Store: Processed over 1.38 million transactional rows into a structured analytical feature table (product_reorder_posterior.csv) containing posterior parameters ($\alpha, \beta$), raw vs. posterior means, and exact 95% Credible Interval widths (ci_width).Live Microservice API: Deployed a lightweight Python/FastAPI backend containerized on Render that computes real-time High-Density Intervals (HDI) and risk classifications from incoming payload requests.Dynamic BI Integration: Connected Power BI to the Render FastAPI microservice using custom M-code (Web.Contents), allowing live parameters to dynamically update report gauge visuals and risk KPI cards.🛠️ Tech StackLanguage: Python 3.10+Backend & API: FastAPI, Uvicorn, PydanticData Processing & Stats: Pandas, NumPy, SciPyBusiness Intelligence: Power BI Desktop, M-Code / Power QueryDeployment & Hosting: Render, GitHub📊 Dashboard StructureThe Power BI report (bayesian_estimator.pbix) consists of 5 specialized pages:01 Executive Overview: Macro-level transactional volume, department distributions, and global reorder performance.02 Bayesian Reorder Analysis: Visualizing shrinkage effects, uncertainty bounds (ci_width), and posterior distributions against raw rates.03 Product Reorder Audit: Searchable audit grid with dynamic cross-filtering across aisles and departments.04 Strategic Insights: Executive recommendations for stock prioritization, safety buffers, and targeted promotions.05 Real-Time Inventory API: Parameterized inspection interface connected to the live Render endpoint displaying dynamic 95% HDI gauge bounds and risk categorization.🚀 Live API ReferenceEndpoint: Estimate Stock ConfidenceMethod: POSTURL: [https://bayesian-estimator-mhpy.onrender.com/estimate/stock-confidence](https://bayesian-estimator-mhpy.onrender.com/estimate/stock-confidence)Swagger Docs: [https://bayesian-estimator-mhpy.onrender.com/docs](https://bayesian-estimator-mhpy.onrender.com/docs)Request Body PayloadJSON{
  "prior_alpha": 2.0,
  "prior_beta": 8.0,
  "picking_attempts": 100,
  "reported_discrepancies": 12
}
JSON Response PayloadJSON{
  "posterior_alpha": 14.0,
  "posterior_beta": 96.0,
  "posterior_mean": 0.1273,
  "hdi_95_lower": 0.0720,
  "hdi_95_upper": 0.1953,
  "stock_risk_category": "MODERATE_MISCOUNT_RISK"
}
💻 Local Setup & Installation1. Clone Repository & Install DependenciesBashgit clone https://github.com/your-username/bayesian-inventory-risk-engine.git
cd bayesian-inventory-risk-engine
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
2. Run API Server LocallyBashuvicorn main:app --reload
Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to inspect the interactive Swagger UI.3. Open DashboardOpen bayesian_estimator.pbix in Power BI Desktop. Ensure active internet connectivity to perform live data refreshes against the Render backend endpoint.
