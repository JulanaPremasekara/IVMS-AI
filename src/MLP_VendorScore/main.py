import torch
import torch.nn as nn
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union # Added for handling lists of vendors

# 1. DEFINE THE MODEL ARCHITECTURE
# This structure must match the training script exactly.
class VendorMLP(nn.Module):
    def __init__(self):
        super(VendorMLP, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 32), # 6 inputs (Status, Delay, etc.)
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)  # 1 output (The Score)
        )
    def forward(self, x):
        return self.net(x)

# 2. INITIALIZE APP AND LOAD ASSETS
app = FastAPI(title="Vendor Selection API")

# Load the saved model weights (.pth)
model = VendorMLP()
model.load_state_dict(torch.load("vendor_mlp_model.pth"))
model.eval() # Set to evaluation mode (turns off dropout/batchnorm)

# Load the scalers (.pkl) used during training to keep data consistent
f_scaler = joblib.load("feature_scaler.pkl")
t_scaler = joblib.load("target_scaler.pkl")

# 3. DEFINE THE DATA STRUCTURE
class VendorInput(BaseModel):
    status: float
    delivery_delay: float
    lead_time: float
    is_weekend: float
    damage_rate: float
    fill_rate: float

# 4. THE ENDPOINT
# Updated to accept either a single vendor OR a list [] of vendors
@app.post("/predict")
def predict_score(data: Union[VendorInput, List[VendorInput]]):
    
    # Check if the incoming data is a single object; if so, wrap it in a list
    if not isinstance(data, list):
        data = [data]

    # Step A: Extract features from the list of objects into a 2D array
    raw_features = [[
        v.status, 
        v.delivery_delay, 
        v.lead_time, 
        v.is_weekend, 
        v.damage_rate, 
        v.fill_rate
    ] for v in data]
    
    # Step B: Scale features (The model only understands data in the 0-1 or -1-1 range)
    scaled_features = f_scaler.transform(raw_features)
    input_tensor = torch.tensor(scaled_features, dtype=torch.float32)
    
    # Step C: Get prediction from the model
    with torch.no_grad(): # No need to calculate gradients for inference (saves memory)
        prediction_scaled = model(input_tensor).numpy()
        
        # Step D: Un-scale the prediction back to the original range (e.g., 0 to 100)
        final_scores = t_scaler.inverse_transform(prediction_scaled)
    
    # Step E: Format the scores into a readable list
    score_list = [round(float(s[0]), 2) for s in final_scores]

    # Step F: Logic to find the Best Vendor
    # We find the highest score and its position (index) in the list
    best_score = max(score_list)
    best_index = score_list.index(best_score)

    # Return the comparison results
    return {
        "all_scores": score_list,
        "best_vendor_index": best_index,
        "best_vendor_score": best_score,
        "recommendation": f"Vendor at index {best_index} is the best choice."
    }

# --- HOW TO RUN ---
# 1. Open Terminal in your project folder
# 2. Run: python -m uvicorn main:app --reload
# 3. Use Postman to POST a JSON list to: http://127.0.0.1:8000/predict