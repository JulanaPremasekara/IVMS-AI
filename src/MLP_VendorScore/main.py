import torch
import torch.nn as nn
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

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
def predict_score(data: VendorInput):
    # Step A: Convert the JSON input into a list for the scaler
    raw_features = [[
        data.status, 
        data.delivery_delay, 
        data.lead_time, 
        data.is_weekend, 
        data.damage_rate, 
        data.fill_rate
    ]]
    
    # Step B: Scale the features (Model expects scaled numbers)
    scaled_features = f_scaler.transform(raw_features)
    input_tensor = torch.tensor(scaled_features, dtype=torch.float32)
    
    # Step C: Get prediction from the model
    with torch.no_grad():
        prediction_scaled = model(input_tensor).numpy()
        
        # Step D: Un-scale the prediction back to 0-100 range
        final_score = t_scaler.inverse_transform(prediction_scaled)
    
    # Return the result as a dictionary (FastAPI converts this to JSON)
    return {
        "vendor_score": round(float(final_score[0][0]), 2),
        "status": "success"
    }

# TO RUN: Open your terminal and type: 
# uvicorn main:app --reload