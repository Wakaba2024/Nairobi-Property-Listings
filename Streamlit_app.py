import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------------
# Load Model
# -----------------------
saved_model = joblib.load("model.pkl")

model = saved_model["model"]
mae = saved_model["mae"]
feature_columns = saved_model["features"]

# -----------------------
# App Title
# -----------------------
st.title("🏠 Nairobi Property Price Predictor")

st.write("Predict property prices using machine learning.")

# -----------------------
# Inputs
# -----------------------
location = st.selectbox(
    "Select Location",
    ["lavington", "kilimani", "westlands area",
     "kileleshwa", "runda", "karen",
     "loresho", "kitisuru", "riverside",
     "langata", "lower kabete", "other"]
)

bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)
size = st.number_input("Size (sqm)", min_value=20, max_value=2000, value=120)
amenity_score = st.slider("Amenity Score", 0, 30, 10)

# -----------------------
# Prepare Input Data
# -----------------------
input_data = pd.DataFrame({
    "Bedrooms": [bedrooms],
    "Bathrooms": [bathrooms],
    "Size (sqm)": [size],
    "amenity_score": [amenity_score],
    "Location": [location]
})

# One-hot encode location
input_data = pd.get_dummies(input_data)

# Align with training features
for col in feature_columns:
    if col not in input_data:
        input_data[col] = 0

input_data = input_data[feature_columns]

# -----------------------
# Predict
# -----------------------
if st.button("Predict Price"):

    prediction = model.predict(input_data)[0]

    lower_bound = prediction - mae
    upper_bound = prediction + mae

    st.subheader("💰 Prediction Result")
    st.write(f"Predicted Price: **KES {prediction:,.0f}**")

    st.write(
        f"Estimated Range: KES {lower_bound:,.0f} - KES {upper_bound:,.0f}"
    )

    st.subheader("📊 Price Drivers")
    st.write(
        "The prediction is primarily influenced by property size, "
        "location, number of bedrooms/bathrooms, and amenity score. "
        "Premium locations and larger sizes typically increase price."
    )
    