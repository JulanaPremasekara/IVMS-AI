from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Demand Forecasting API")

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "lightgbm_model.pkl")

model_columns_path = BASE_DIR / "model_columns.pkl"
model_rmse_path = BASE_DIR / "model_rmse.pkl"
target_min_path = BASE_DIR / "target_min.pkl"
target_max_path = BASE_DIR / "target_max.pkl"

model_columns = joblib.load(model_columns_path) if model_columns_path.exists() else [
    "UNIT_PRICE",
    "INITIAL_STOCK",
    "REORDER_THRESHOLD",
    "IS_WEEKEND",
    "MONTH",
    "CAT_Digital Devices",
    "CAT_Electronics",
    "CAT_Home appliances",
    "CAT_Kitchen Appliances",
    "CAT_Personal Care",
]

model_rmse = joblib.load(model_rmse_path) if model_rmse_path.exists() else None
target_min = joblib.load(target_min_path) if target_min_path.exists() else 0.0
target_max = joblib.load(target_max_path) if target_max_path.exists() else 1.0


# -------------------------------
# Validation Error Handler
# -------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid input data",
            "details": exc.errors()
        }
    )


# -------------------------------
# Input Validation Model
# -------------------------------
class InputData(BaseModel):
    UNIT_PRICE: float = Field(..., gt=0, description="Must be greater than 0")
    INITIAL_STOCK: float = Field(..., ge=0, description="Cannot be negative")
    REORDER_THRESHOLD: float = Field(..., ge=0, description="Cannot be negative")

    IS_WEEKEND: int = Field(..., ge=0, le=1, description="Only 0 or 1 allowed")
    MONTH: int = Field(..., ge=1, le=12, description="Month must be between 1 and 12")

    CAT_Digital_Devices: int = Field(..., ge=0, le=1)
    CAT_Electronics: int = Field(..., ge=0, le=1)
    CAT_Home_appliances: int = Field(..., ge=0, le=1)
    CAT_Kitchen_Appliances: int = Field(..., ge=0, le=1)
    CAT_Personal_Care: int = Field(..., ge=0, le=1)

    # Extra simple validation
    @field_validator(
        "CAT_Digital_Devices",
        "CAT_Electronics",
        "CAT_Home_appliances",
        "CAT_Kitchen_Appliances",
        "CAT_Personal_Care"
    )
    @classmethod
    def validate_category_values(cls, value):
        if value not in [0, 1]:
            raise ValueError("Category values must be only 0 or 1")
        return value


# -------------------------------
# Home Route
# -------------------------------
@app.get("/")
def home():
    return {"message": "LightGBM Demand Forecasting API is running!"}


# -------------------------------
# Prediction Route
# -------------------------------
@app.post("/predict")
def predict(data: InputData):
    try:
        input_dict = {
            "UNIT_PRICE": data.UNIT_PRICE,
            "INITIAL_STOCK": data.INITIAL_STOCK,
            "REORDER_THRESHOLD": data.REORDER_THRESHOLD,
            "IS_WEEKEND": data.IS_WEEKEND,
            "MONTH": data.MONTH,
            "CAT_Digital Devices": data.CAT_Digital_Devices,
            "CAT_Electronics": data.CAT_Electronics,
            "CAT_Home appliances": data.CAT_Home_appliances,
            "CAT_Kitchen Appliances": data.CAT_Kitchen_Appliances,
            "CAT_Personal Care": data.CAT_Personal_Care,
        }

        input_df = pd.DataFrame([input_dict])
        input_df = input_df[model_columns]

        prediction = model.predict(input_df)
        predicted_value = float(prediction[0])

        # Demand Label
        if predicted_value < 0.3:
            demand_label = "Low Demand"
        elif predicted_value < 0.6:
            demand_label = "Medium Demand"
        else:
            demand_label = "High Demand"

        response = {
            "prediction": round(predicted_value, 2),
            "interpretation": demand_label
        }

        # Confidence Range
        if model_rmse is not None:
            lower_bound = max(float(target_min), predicted_value - float(model_rmse))
            upper_bound = min(float(target_max), predicted_value + float(model_rmse))

            target_range = float(target_max) - float(target_min)

            if target_range > 0:
                confidence_percent = max(
                    0.0,
                    100 * (1 - (float(model_rmse) / target_range))
                )
            else:
                confidence_percent = 100.0

            if confidence_percent >= 80:
                confidence_level = "High"
            elif confidence_percent >= 60:
                confidence_level = "Medium"
            else:
                confidence_level = "Low"

            response["estimated_range"] = {
                "lower": round(lower_bound, 2),
                "upper": round(upper_bound, 2)
            }

            response["estimated_confidence"] = {
                "score_percent": round(confidence_percent, 2),
                "level": confidence_level
            }

        return response

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Prediction failed",
                "details": str(e)
            }
        )