from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")

columns = [c for c in columns if c != "actual_price"]

class ProductData(BaseModel):
    category: str
    discounted_price: float
    discount_percentage: float
    rating: float
    rating_count: int

@app.post("/predict")
def predict(data: ProductData):

    input_data = pd.DataFrame(0, index=[0], columns=columns)

    input_data["discounted_price"] = data.discounted_price
    input_data["discount_percentage"] = data.discount_percentage
    input_data["rating"] = data.rating
    input_data["rating_count"] = data.rating_count

    if data.category in input_data.columns:
        input_data[data.category] = 1

    prediction = model.predict(input_data)[0]

    return {
        "predicted_price": float(prediction)
    }