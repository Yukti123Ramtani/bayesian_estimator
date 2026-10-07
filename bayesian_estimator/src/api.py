from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from src.estimator import BayesianInventoryEstimator

app = FastAPI(
    title="Bayesian Inventory Noise Estimator API",
    description="Microservice evaluating true stock depletion vs human picking errors.",
    version="1.0.0"
)


class InventoryInspectionRequest(BaseModel):
    prior_alpha: float = Field(default=2.0, gt=0, description="Prior Beta alpha shape parameter")
    prior_beta: float = Field(default=8.0, gt=0, description="Prior Beta beta shape parameter")
    picking_attempts: int = Field(..., ge=1, description="Total picking attempts in batch")
    reported_discrepancies: int = Field(..., ge=0, description="Reported inventory discrepancies")


class InventoryInspectionResponse(BaseModel):
    posterior_alpha: float
    posterior_beta: float
    posterior_mean: float
    hdi_95_lower: float
    hdi_95_upper: float
    stock_risk_category: str


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "service": "Bayesian Inventory Estimator"}


@app.post("/estimate/stock-confidence", response_model=InventoryInspectionResponse, status_code=status.HTTP_200_OK)
def calculate_stock_confidence(payload: InventoryInspectionRequest):
    if payload.reported_discrepancies > payload.picking_attempts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reported_discrepancies cannot be greater than picking_attempts"
        )

    try:
        estimator = BayesianInventoryEstimator(
            prior_alpha=payload.prior_alpha,
            prior_beta=payload.prior_beta
        )
        results = estimator.compute_metrics(
            picking_attempts=payload.picking_attempts,
            reported_discrepancies=payload.reported_discrepancies
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )