# 🏠 Nairobi Property Price Prediction & Market Intelligence

------------------------------------------------------------------------

## 1️⃣ Overview and Problem Statement

This project builds a complete end-to-end machine learning pipeline to
analyze and predict property prices in Nairobi, Kenya.

The objective was to:

-   Scrape real estate listings
-   Clean and engineer meaningful features
-   Understand key price drivers
-   Train predictive models
-   Deploy a pricing app
-   Build a business-ready dashboard

Key business questions addressed:

-   Which locations are most expensive?
-   How strongly does size influence property price?
-   Do amenities significantly increase value?
-   Can we accurately predict property prices using ML?

This project demonstrates a full ML lifecycle from data acquisition to
deployment.

------------------------------------------------------------------------

## 2️⃣ Project Structure

    NAIROBI_HOUSE_PRICE_SPRINT/
    │
    ├── data/
    │   ├── clean_listings.csv
    │   ├── data_dictionary.csv
    │   └── nairobi_combined_all_listings.csv
    │
    ├── Notebooks/
    │   ├── data_cleaning.ipynb
    │   ├── Modelling_Baseline.ipynb
    │   └── Model_Improvement.ipynb
    │
    ├── Dashboard.py
    ├── Streamlit_app.py
    ├── Scrapper.py
    ├── main.py
    ├── model.pkl
    ├── pyproject.toml
    ├── uv.lock
    └── README.md

------------------------------------------------------------------------

## 3️⃣ Features

### 🔹 Data Collection

-   Custom web scraper for Nairobi property listings
-   Extracted structured real estate attributes

### 🔹 Data Cleaning & Feature Engineering

-   Removed duplicates
-   Standardized location names
-   Imputed missing size values (location-based averages)
-   Removed invalid sizes and outliers
-   Created engineered features:
    -   `price_per_sqft`
    -   `amenity_score`
    -   `month`
    -   `year`
    -   `size_sqft`

### 🔹 Modeling

-   Linear Regression (baseline)
-   Random Forest
-   XGBoost
-   Model comparison using MAE, RMSE, and R²

### 🔹 Deployment

-   Streamlit Pricing App
-   Executive Market Dashboard
-   KPI cards and interactive filters

------------------------------------------------------------------------

## 4️⃣ Installation and Usage

### 🔹 Clone Repository

``` bash
git clone https://github.com/Wakaba2024/Nairobi-Property-Listings.git
cd Nairobi-Property-Listings
```

### 🔹 Install Dependencies

``` bash
pip install -r requirements.txt
```

or using uv:

``` bash
uv sync
```

### 🔹 Run Pricing App

``` bash
streamlit run Streamlit_app.py
```

### 🔹 Run Dashboard

``` bash
streamlit run Dashboard.py
```

------------------------------------------------------------------------

## 5️⃣ Results and Key Insights

-   Size is the strongest predictor of property price.
-   Premium locations (Lavington, Kilimani, Westlands) command
    significantly higher median prices.
-   Price per square foot provides better cross-location comparison than
    total price.
-   Amenity tiers contribute to value but are secondary to size and
    location.
-   Tree-based models (Random Forest, XGBoost) outperform linear
    regression in capturing non-linear patterns.

------------------------------------------------------------------------

## 6️⃣ Key Errors and Challenges

-   Scraper initially returned 0 listings due to incorrect HTML
    selectors.
-   Encountered `KeyError: 'price_kes'` due to empty dataframe after
    scraping failure.
-   Altair compatibility issue (`altair.vegalite.v4`) caused Streamlit
    import errors.
-   Scikit-learn version mismatch warning when loading saved model.
-   Missing size values required careful imputation strategy.
-   Extreme outliers distorted price_per_sqft calculations.

------------------------------------------------------------------------

