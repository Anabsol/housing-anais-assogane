from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI()

class PredictRequest(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(request: PredictRequest):
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    prediction = model.predict(np.array(request.features).reshape(1, -1))
    return {"prediction": prediction[0]}
