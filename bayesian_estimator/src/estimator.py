import numpy as np
from scipy import stats
from typing import Dict, Any, Tuple


class BayesianInventoryEstimator:
    """
    Beta-Binomial Conjugate Model for Inventory Miscount Filtering.
    Estimates true stock discrepancy probability given picking history and noise.
    """

    def __init__(self, prior_alpha: float = 2.0, prior_beta: float = 8.0):
        if prior_alpha <= 0 or prior_beta <= 0:
            raise ValueError("Prior alpha and beta must be positive numbers.")
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta

    def update_posterior(self, picking_attempts: int, reported_discrepancies: int) -> Tuple[float, float]:
        """Calculates updated Beta parameters based on new batch data."""
        if reported_discrepancies > picking_attempts:
            raise ValueError("Discrepancies cannot exceed total attempts.")

        post_alpha = self.prior_alpha + reported_discrepancies
        post_beta = self.prior_beta + (picking_attempts - reported_discrepancies)
        return post_alpha, post_beta

    def compute_metrics(self, picking_attempts: int, reported_discrepancies: int) -> Dict[str, Any]:
        """Calculates posterior mean, 95% High-Density Interval (HDI), and risk category."""
        post_a, post_b = self.update_posterior(picking_attempts, reported_discrepancies)

        # Point Estimate (Posterior Mean)
        post_mean = post_a / (post_a + post_b)

        # 95% Credible Interval using Beta Percentile Point Function (ppf)
        hdi_lower = float(stats.beta.ppf(0.025, post_a, post_b))
        hdi_upper = float(stats.beta.ppf(0.975, post_a, post_b))

        # Risk Classification Logic
        if post_mean < 0.10:
            risk_category = "LOW_MISCOUNT_RISK"
        elif post_mean < 0.25:
            risk_category = "MODERATE_MISCOUNT_RISK"
        else:
            risk_category = "HIGH_INVENTORY_DEPLETION_RISK"

        return {
            "posterior_alpha": round(post_a, 4),
            "posterior_beta": round(post_b, 4),
            "posterior_mean": round(post_mean, 4),
            "hdi_95_lower": round(hdi_lower, 4),
            "hdi_95_upper": round(hdi_upper, 4),
            "stock_risk_category": risk_category
        }