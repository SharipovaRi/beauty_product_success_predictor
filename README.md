# AI Beauty Product Success Predictor

An end-to-end machine learning application that predicts whether a beauty product is likely to become successful based on historical Sephora product data. The system analyzes pricing, brand performance, product categories, ingredients, and market-positioning features to estimate a product's success probability and identify the factors that contribute most to the prediction.

## Project Overview

Beauty brands regularly introduce new products, but it can be difficult to know how well a product will perform before it reaches the market. Pricing, category competition, ingredients, brand reputation, and product claims can all influence customer interest and overall performance.

This project uses historical Sephora product data to build a machine learning model that predicts whether a new product is likely to be successful based on its characteristics. Product success is determined using historical product performance metrics, including customer ratings, review activity, and consumer engagement.

The system analyzes:

* Brand
* Product category
* Price
* Ingredients
* Product claims and highlights
* Sephora-exclusive status
* Limited-edition status
* Category competition
* Brand historical performance
* Ingredient popularity 

The model returns:

* Success probability
* Predicted outcome
* Confidence band
* Top positive prediction factors
* Top negative prediction factors
* Local prediction explanations

## Key Features
### Currently Available 
* End-to-end machine learning pipeline
* Real Sephora beauty product dataset
* Advanced feature engineering
* Model comparison and selection
* Prediction explainability
* FastAPI backend service
### Planned Features
* AI-powered product strategy recommendations
* AI chatbot assistant
* Interactive Next.js frontend
* Containerized deployment 

## Business Problem

Launching a beauty product requires a significant investment in product development, manufacturing, inventory, and marketing. Because of these costs, brands want to understand how a product is likely to perform before committing resources to a launch.
This project helps evaluate new product concepts by comparing them with historical product patterns. The model identifies characteristics that are commonly associated with successful products and estimates the likelihood that a new product will achieve similar results.

The goal is to provide an additional data point that can support product development and product positioning decisions.


## Dataset

The project uses real beauty product data with columns including:

* product_id
* product_name
* brand_name
* loves_count
* rating
* reviews
* ingredients
* price_usd
* sale_price_usd
* limited_edition
* new
* online_only
* out_of_stock
* sephora_exclusive
* highlights
* primary_category
* secondary_category
* tertiary_category
* child_count
* child_max_price
* child_min_price

## Feature Engineering

The feature engineering pipeline transforms raw Sephora product data into model-ready business, pricing, ingredient, brand, category, and text features.

### Product-Level Features

These features describe the product itself:

* `ingredient_count`: number of ingredients in the product formula
* `highlight_count`: number of marketing claims/highlights
* `product_name_length`: length of the product name
* `ingredients_text_length`: length of the ingredient list
* `highlights_text_length`: length of the highlights/claims text
* `has_variation`: whether the product has variations such as shades or formats
* `has_size`: whether size information is available
* `has_child_products`: whether the product belongs to a product family
*  `child_price_range`: price range across child products

### Pricing Features

These features capture pricing strategy and market positioning:

* `price_tier`: budget, mid-range, premium, or luxury
* `has_sale_price`: whether the product has a sale price
* `discount_amount`: difference between regular price and sale price
* `discount_pct`: percentage discount
* `value_price_gap`: difference between value price and actual price
* `price_vs_category_avg`: product price compared to category average
* `price_vs_brand_avg`: product price compared to brand average

### Ingredient Features

The system tracks popular beauty/skincare ingredients based on common product claims and consumer interest, including:

* niacinamide
* retinol
* hyaluronic acid
* salicylic acid
* glycolic acid
* vitamin c
* ascorbic acid
* peptides
* ceramides
* squalane
* glycerin
* panthenol
* zinc
* lactic acid
* azelaic acid
* centella
* green tea
* aloe

Each ingredient is converted into a binary indicator feature, such as:

```
contains_niacinamide
contains_retinol
contains_hyaluronic_acid
```
The pipeline also creates `popular_ingredient_count`, which measures how many tracked high-interest ingredients are present in a product.

### Brand Features
* `brand_product_count`
* `brand_avg_price`
* `brand_success_rate`
* `brand_limited_edition_rate`
* `brand_sephora_exclusive_rate`

### Category Features
* `category_product_count`
* `category_avg_price`
* `category_success_rate`
* `category_saturation_score`
* `category_sephora_exclusive_rate`

### Secondary Category Features
* `secondary_category_product_count`
* `secondary_category_avg_price`
* `secondary_category_success_rate`

### Text Features
A combined product_text field is created from:
* product name
* brand name
* primary category
* secondary category
* tertiary category
* ingredients
* highlights
* variation description

The combined text field is transformed using TF-IDF during model training, allowing the model to learn patterns from product descriptions, ingredient terminology, category information, and marketing claims.

## Model Development

The project compares multiple machine learning models before selecting the final model.

Models compared:
* Logistic Regression
* Random Forest
* XGBoost

Evaluation metrics:

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC

The final model is selected based on cross-validated F1-score.

**Current Best Model**: Logistic Regression

Although tree-based models were evaluated, Logistic Regression achieved the highest cross-validated F1-score. The model performs well on the sparse, high-dimensional feature space created by TF-IDF text representations and engineered categorical features.

## Tech Stack
### Data & Machine Learning
* Python
* Pandas
* NumPy
* Scikit-Learn
* TF-IDF
* Logistic Regression
* Random Forest
* XGBoost
### Backend
* FastAPI
* Pydantic
* Uvicorn
* Joblib
### Frontend (Planned)
* Next.js
* React
* TypeScript
### Deployment (Planned)
* Docker
* Railway 

## Current Status
This project is currently under active development.

### Completed:

* Data cleaning pipeline
* Feature engineering pipeline
* Model comparison
* Final model training
* FastAPI prediction endpoint
* Local prediction explanations

### In progress:

* AI launch insight generator
* AI product strategy chatbot
* Next.js frontend
* Deployment

## Disclaimer

This project is a product analytics and machine learning portfolio project. Predictions are based on historical product patterns from public beauty product data.
The system does not provide medical, dermatology, allergy, or cosmetic safety advice. Model outputs should be interpreted as business/product strategy estimates, not guaranteed product outcomes.