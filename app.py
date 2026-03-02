from fastapi import FastAPI
import pandas as pd
import numpy as np

app = FastAPI(title="Customer Intelligence API")

# Load your prediction & simulation data (replace with actual CSV if needed)
df_predictions = pd.read_csv("df_predictions.csv")  # customer_id, churn_prob
df_simulation = pd.read_csv("df_simulation.csv")    # expected revenue, ROI, etc.

@app.get("/")
def read_root():
    return {"message": "Customer Intelligence API is running!"}

@app.get("/churn/{customer_id}")
def get_churn(customer_id: str):
    record = df_predictions[df_predictions["customer_id"] == customer_id]
    if record.empty:
        return {"error": "Customer not found"}
    return record.to_dict(orient="records")[0]

@app.get("/simulation/{customer_id}")
def get_simulation(customer_id: str):
    record = df_simulation[df_simulation["customer_id"] == customer_id]
    if record.empty:
        return {"error": "Customer not found"}
    return record.to_dict(orient="records")[0]

@app.get("/dashboard_summary")
def dashboard_summary():
    total_expected_revenue = df_simulation["expected_revenue"].sum()
    total_discount_cost = df_simulation["discount_cost"].sum()
    avg_roi = (total_expected_revenue - total_discount_cost) / total_discount_cost
    return {
        "total_expected_revenue": total_expected_revenue,
        "total_discount_cost": total_discount_cost,
        "avg_roi_percent": avg_roi * 100
    }