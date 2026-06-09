import streamlit as st
import pandas as pd
import joblib
import requests



columns = joblib.load("columns1.pkl")


# REMOVE TARGET if mistakenly saved
columns = [c for c in columns if c != "actual_price"]

st.title("Amazon Price Prediction")

discounted_price = st.number_input("Discounted Price", value=500.0)
discount_percentage = st.number_input("Discount Percentage", value=10.0)
rating = st.number_input("Rating", value=4.0)
rating_count = st.number_input("Rating Count", value=100)

category = st.selectbox("Category", [c for c in columns if "category_" in c])

if st.button("Predict"):

    url = "http://127.0.0.1:8000/predict"

    data = {
        "category": category,
        "discounted_price": discounted_price,
        "discount_percentage": discount_percentage,
        "rating": rating,
        "rating_count": int(rating_count)
    }

    response = requests.post(url, json=data)

    result = response.json()

    st.success(
        f"Predicted Price: ₹{result['predicted_price']:.2f}"
    )