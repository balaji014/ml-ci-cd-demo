# src/app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

MODEL_PATH = "model/model.pkl"

# Define the input data model using Pydantic


class InputData(BaseModel):
    x: float


# Initialize FastAPI app
app = FastAPI()

# Load the trained model
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/predict")
def predict(data: InputData):
    """Make a prediction"""
    x_value = np.array([[data.x]])
    prediction = model.predict(x_value)
    return {"prediction": prediction[0]}
