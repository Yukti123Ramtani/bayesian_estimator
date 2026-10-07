import os
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

PRIOR_STRENGTH = 20.0  # Pseudo-observations

def build_data():
    data_file = Path(os.environ.get("DATA_FILE", "product_reorder_posterior.csv"))
    out_dir = Path(os.environ.get("OUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load aggregated data
    df = pd.read_csv(data_file)
    df["times_reordered"] = df["times_reordered"].astype("int64")

    # Recompute volume-weighted aisle rates
    aisle_stats = df.groupby("aisle")[["times_reordered", "times_ordered"]].sum()
    aisle_stats["aisle_rate"] = aisle_stats["times_reordered"] / aisle_stats["times_ordered"]

    if "aisle_reorder_rate" in df.columns:
        df = df.drop(columns=["aisle_reorder_rate"])

    df = df.merge(aisle_stats[["aisle_rate"]], left_on="aisle", right_index=True, how="left")

    # Bayesian Beta-Binomial Update
    df["prior_alpha"] = PRIOR_STRENGTH * df["aisle_rate"]
    df["prior_beta"] = PRIOR_STRENGTH * (1.0 - df["aisle_rate"])
    df["post_alpha"] = df["prior_alpha"] + df["times_reordered"]
    df["post_beta"] = df["prior_beta"] + (df["times_ordered"] - df["times_reordered"])

    df["raw_rate"] = df["times_reordered"] / df["times_ordered"]
    df["posterior_mean"] = df["post_alpha"] / (df["post_alpha"] + df["post_beta"])

    tail = (1.0 - 0.95) / 2.0
    df["ci_lower"] = stats.beta.ppf(tail, df["post_alpha"], df["post_beta"])
    df["ci_upper"] = stats.beta.ppf(1.0 - tail, df["post_alpha"], df["post_beta"])
    df["ci_width"] = df["ci_upper"] - df["ci_lower"]
    df["low_data"] = df["times_ordered"] < 10

    export_cols = [
        "product_id", "product_name", "aisle", "department",
        "times_ordered", "times_reordered", "raw_rate",
        "prior_alpha", "prior_beta", "post_alpha", "post_beta",
        "posterior_mean", "ci_lower", "ci_upper", "ci_width", "low_data"
    ]
    df[export_cols].round(4).to_csv(out_dir / "product_reorder_posteriors.csv", index=False)
    print(f"Exported processing results to {out_dir.resolve()}")

if __name__ == "__main__":
    build_data()