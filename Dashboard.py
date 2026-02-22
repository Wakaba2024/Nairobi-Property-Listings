import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(layout="wide")
st.title("🏠 Nairobi Property Market Dashboard")

# -----------------------------------
# Load Data
# -----------------------------------
df = pd.read_csv(r"C:\Users\user\Nairobi_House_Price_Sprint\data\clean_listings.csv")

# Ensure proper formats
df["Listing Date"] = pd.to_datetime(df["Listing Date"], errors="coerce")
df["Location"] = df["Location"].str.lower()

# -----------------------------------
# Sidebar Filters
# -----------------------------------
st.sidebar.header("Filters")

selected_locations = st.sidebar.multiselect(
    "Select Locations",
    options=sorted(df["Location"].unique()),
    default=sorted(df["Location"].unique())
)

selected_property_type = st.sidebar.multiselect(
    "Select Property Type",
    options=sorted(df["Property Type"].unique()),
    default=sorted(df["Property Type"].unique())
)

df = df[
    (df["Location"].isin(selected_locations)) &
    (df["Property Type"].isin(selected_property_type))
]

# -----------------------------------
# KPI Section
# -----------------------------------
st.subheader("📊 Market Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Listings", len(df))
col2.metric("Median Price (KES)", f"{int(df['Price (KES)'].median()):,}")
col3.metric("Avg Price per Sqft", f"{int(df['price_per_sqft'].mean()):,}")
col4.metric("Median Bedrooms", int(df["Bedrooms"].median()))

st.divider()

# -----------------------------------
# 1️⃣ Median Price by Location
# -----------------------------------
st.header("📍 Median Price by Location")

if not df.empty:
    median_prices = (
        df.groupby("Location")["Price (KES)"]
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig1 = px.bar(
        median_prices,
        x="Location",
        y="Price (KES)",
        text_auto=True,
        title="Median Property Price by Location"
    )

    st.plotly_chart(fig1, use_container_width=True)

st.divider()

# -----------------------------------
# 2️⃣ Monthly Price Trend
# -----------------------------------
st.header("📈 Monthly Price Trend")

if df["Listing Date"].notna().sum() > 0:
    df["Month"] = df["Listing Date"].dt.to_period("M")
    monthly_trend = (
        df.groupby("Month")["Price (KES)"]
        .median()
        .reset_index()
    )

    monthly_trend["Month"] = monthly_trend["Month"].astype(str)

    fig2 = px.line(
        monthly_trend,
        x="Month",
        y="Price (KES)",
        markers=True,
        title="Median Price Trend Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -----------------------------------
# 3️⃣ Price per Sqft Comparison
# -----------------------------------
st.header("📐 Price per Sqft Comparison")

if "price_per_sqft" in df.columns:
    ppsq = (
        df.groupby("Location")["price_per_sqft"]
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig3 = px.bar(
        ppsq,
        x="Location",
        y="price_per_sqft",
        text_auto=True,
        title="Median Price per Sqft by Location"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# -----------------------------------
# 4️⃣ Amenity Tier Impact Analysis
# -----------------------------------
st.header("🏊 Amenity Impact on Price")

if "amenity_score" in df.columns and df["amenity_score"].nunique() > 1:

    df["amenity_band"] = pd.qcut(
        df["amenity_score"],
        q=3,
        labels=["Low", "Medium", "High"]
    )

    amenity_analysis = (
        df.groupby("amenity_band")["Price (KES)"]
        .median()
        .reset_index()
    )

    fig4 = px.bar(
        amenity_analysis,
        x="amenity_band",
        y="Price (KES)",
        text_auto=True,
        title="Median Price by Amenity Tier"
    )

    st.plotly_chart(fig4, use_container_width=True)

else:
    st.warning("Not enough variation in amenity scores to analyze impact.")

st.divider()

# -----------------------------------
# Executive Insights
# -----------------------------------
st.header("📌 Executive Insights")

st.write("""
- Premium neighborhoods such as Lavington, Kilimani, and Westlands dominate pricing.
- Price per square foot varies significantly, indicating strong location-based value density.
- Monthly price movements suggest volatility in upper-market segments.
- Amenity tiers contribute to value, but location and property size remain primary drivers.
""")