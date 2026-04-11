import torch
import torch.nn as nn
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union

# 1. DEFINE THE MODEL ARCHITECTURE
# This must match exactly the structure you used during training.
class VendorMLP(nn.Module):
    def __init__(self):
        super(VendorMLP, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
    def forward(self, x):
        return self.net(x)

# 2. INITIALIZE APP AND LOAD ASSETS
app = FastAPI(title="Vendor Selection API")

# Load the saved model and weights
model = VendorMLP()
model.load_state_dict(torch.load("vendor_mlp_model.pth"))
model.eval() # Set to evaluation mode

# Load the scalers
f_scaler = joblib.load("feature_scaler.pkl")
t_scaler = joblib.load("target_scaler.pkl")

# 3. DEFINE THE DATA STRUCTURE (The order/format of incoming data)
class VendorInput(BaseModel):
    status: float
    delivery_delay: float
    lead_time: float
    is_weekend: float
    damage_rate: float
    fill_rate: float

# 4. THE ENDPOINT
@app.post("/predict")
def predict_score(data: Union[VendorInput, List[VendorInput]]):
    # Ensure data is always a list for processing
    if not isinstance(data, list):
        data = [data]

    # 1. Extract and Scale Data
    raw_inputs = [[
        v.status, v.delivery_delay, v.lead_time,
        v.is_weekend, v.damage_rate, v.fill_rate
    ] for v in data]

    scaled_inputs = f_scaler.transform(raw_inputs)
    tensor_inputs = torch.tensor(scaled_inputs, dtype=torch.float32)

    # 2. Get Predictions
    with torch.no_grad():
        prediction_scaled = model(tensor_inputs).numpy()
        final_scores = t_scaler.inverse_transform(prediction_scaled)

    # Convert scores to a flat list of floats
    score_list = [round(float(s[0]), 2) for s in final_scores]

    # 3. IDENTIFY THE BEST VENDOR
    # Find the index of the highest score (e.g., Index 0, 1, or 2)
    best_score = max(score_list)
    best_index = score_list.index(best_score)

    return {
        "all_scores": score_list,
        "best_vendor_index": best_index,
        "best_vendor_score": best_score,
        "recommendation": f"Vendor at index {best_index} is your best choice!"
    }
# TO RUN: Open your terminal and type: 
# uvicorn main:app --reload