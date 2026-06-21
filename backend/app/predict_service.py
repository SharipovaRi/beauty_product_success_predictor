import joblib
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "product_success_pipeline.pkl"
DATA_PATH = BASE_DIR / "data" / "processed" / "beauty_products_features.csv"


model_bundle = joblib.load(MODEL_PATH)
pipeline = model_bundle["pipeline"]
# Historical dataset used for brand-level adn category-level features. 
historical_df = pd.read_csv(DATA_PATH)


POPULAR_INGREDIENTS = [
    "niacinamide",
    "retinol",
    "hyaluronic acid",
    "salicylic acid",
    "glycolic acid",
    "vitamin c",
    "ascorbic acid",
    "peptide",
    "ceramide",
    "squalane",
    "glycerin",
    "panthenol",
    "zinc",
    "lactic acid",
    "azelaic acid",
    "centella",
    "green tea",
    "aloe",
]

# Check if an ingredient is present or not. 
def contains_term(text, term):
    if not text:
        return 0
    return int(term in str(text).lower())

# Count number of ingriedients in the ingredient list.
def count_ingredients(text):
    if not text:
        return 0
    return len([x.strip() for x in str(text).split(",") if x.strip()])

# Categorize price into tiers based on common price ranges in the beauty industry.
def make_price_tier(price):
    if price < 20:
        return "budget"
    elif price < 50:
        return "mid_range"
    elif price < 100:
        return "premium"
    return "luxury"

# All features that were generated during the model training.
def build_features_for_input(product):
    brand = product.brand_name.lower().strip()
    primary_category = product.primary_category.lower().strip()
    secondary_category = product.secondary_category.lower().strip() if product.secondary_category else ""
    tertiary_category = product.tertiary_category.lower().strip() if product.tertiary_category else ""
    variation_type = product.variation_type.lower().strip() if product.variation_type else ""

    ingredients = product.ingredients.lower().strip()
    highlights = product.highlights.lower().strip() if product.highlights else ""
    product_name = product.product_name.lower().strip() if product.product_name else ""

    value_price = product.value_price_usd if product.value_price_usd is not None else product.price_usd
    sale_price = product.sale_price_usd if product.sale_price_usd is not None else 0

    brand_rows = historical_df[historical_df["brand_name"] == brand]
    category_rows = historical_df[historical_df["primary_category"] == primary_category]
    secondary_rows = historical_df[historical_df["secondary_category"] == secondary_category]

    global_success_rate = historical_df["success_label"].mean()
    global_avg_price = historical_df["price_usd"].mean()

    brand_product_count = len(brand_rows) if len(brand_rows) > 0 else 1
    brand_avg_price = brand_rows["price_usd"].mean() if len(brand_rows) > 0 else global_avg_price
    brand_success_rate = brand_rows["success_label"].mean() if len(brand_rows) > 0 else global_success_rate
    brand_limited_edition_rate = brand_rows["limited_edition"].mean() if len(brand_rows) > 0 else historical_df["limited_edition"].mean()
    brand_sephora_exclusive_rate = brand_rows["sephora_exclusive"].mean() if len(brand_rows) > 0 else historical_df["sephora_exclusive"].mean()

    category_product_count = len(category_rows) if len(category_rows) > 0 else 1
    category_avg_price = category_rows["price_usd"].mean() if len(category_rows) > 0 else global_avg_price
    category_success_rate = category_rows["success_label"].mean() if len(category_rows) > 0 else global_success_rate
    category_limited_edition_rate = category_rows["limited_edition"].mean() if len(category_rows) > 0 else historical_df["limited_edition"].mean()
    category_sephora_exclusive_rate = category_rows["sephora_exclusive"].mean() if len(category_rows) > 0 else historical_df["sephora_exclusive"].mean()

    secondary_category_product_count = len(secondary_rows) if len(secondary_rows) > 0 else 1
    secondary_category_avg_price = secondary_rows["price_usd"].mean() if len(secondary_rows) > 0 else global_avg_price
    secondary_category_success_rate = secondary_rows["success_label"].mean() if len(secondary_rows) > 0 else global_success_rate

    discount_amount = product.price_usd - sale_price if sale_price > 0 else 0
    discount_pct = discount_amount / product.price_usd if sale_price > 0 else 0
    value_price_gap = value_price - product.price_usd
    
    # Build feature dictionary for the input product, ensuring all features used in the model training are included and properly calculated based on the input data and historical trends. This includes both raw features from the input and engineered features based on historical data.
    data = {
        "price_usd": product.price_usd,
        "value_price_usd": value_price,
        "sale_price_usd": sale_price,
        "limited_edition": product.limited_edition,
        "new": product.new,
        "online_only": product.online_only,
        "out_of_stock": product.out_of_stock,
        "sephora_exclusive": product.sephora_exclusive,
        "child_count": 0,
        "child_max_price": product.price_usd,
        "child_min_price": product.price_usd,
        "ingredient_count": count_ingredients(ingredients),
        "highlight_count": len([x.strip() for x in highlights.split(",") if x.strip()]),
        "product_name_length": len(product_name),
        "ingredients_text_length": len(ingredients),
        "highlights_text_length": len(highlights),
        "has_sale_price": int(sale_price > 0),
        "discount_amount": discount_amount,
        "discount_pct": discount_pct,
        "value_price_gap": value_price_gap,
        "brand_product_count": brand_product_count,
        "brand_avg_price": brand_avg_price,
        "brand_success_rate": brand_success_rate,
        "brand_limited_edition_rate": brand_limited_edition_rate,
        "brand_sephora_exclusive_rate": brand_sephora_exclusive_rate,
        "category_product_count": category_product_count,
        "category_avg_price": category_avg_price,
        "category_success_rate": category_success_rate,
        "category_limited_edition_rate": category_limited_edition_rate,
        "category_sephora_exclusive_rate": category_sephora_exclusive_rate,
        "secondary_category_product_count": secondary_category_product_count,
        "secondary_category_avg_price": secondary_category_avg_price,
        "secondary_category_success_rate": secondary_category_success_rate,
        "price_vs_category_avg": product.price_usd / category_avg_price,
        "price_vs_brand_avg": product.price_usd / brand_avg_price,
        "category_saturation_score": category_product_count / historical_df["category_product_count"].max(),
        "secondary_category_saturation_score": secondary_category_product_count / historical_df["secondary_category_product_count"].max(),
        "has_variation": int(len(variation_type) > 0),
        "has_size": int(bool(product.size)),
        "has_child_products": 0,
        "child_price_range": 0,
        "brand_name": brand,
        "primary_category": primary_category,
        "secondary_category": secondary_category,
        "tertiary_category": tertiary_category,
        "price_tier": make_price_tier(product.price_usd),
        "variation_type": variation_type,
        "product_text": f"{product_name} {brand} {primary_category} {secondary_category} {tertiary_category} {ingredients} {highlights} {product.variation_desc}",
    }

    popular_count = 0

    # Create binary features for the presence of popular ingredients in the product's ingredient list, which can be important indicators of product success.
    for ingredient in POPULAR_INGREDIENTS:
        col = "contains_" + ingredient.replace(" ", "_")
        value = contains_term(ingredients, ingredient)
        data[col] = value
        popular_count += value

    data["popular_ingredient_count"] = popular_count
    feature_columns = model_bundle["feature_columns"]

    # Create a DataFrame and fill any missing features with default values to ensure the input is complete and compatible with the model.
    X = pd.DataFrame([data])

    for col in feature_columns:
        if col not in X.columns:
            X[col] = 0

    X = X[feature_columns]

    return X

# Generate prediction that will return probability, business label ,and confidence score.
def predict_product(product):
    X = build_features_for_input(product)

    probability = float(pipeline.predict_proba(X)[0][1])

    if probability >= 0.7:
        prediction = "Likely Successful"
    elif probability >= 0.45:
        prediction = "Moderate Potential"
    else:
        prediction = "High Risk"

    if probability >= 0.75 or probability <= 0.25:
        confidence_band = "High"
    elif probability >= 0.6 or probability <= 0.4:
        confidence_band = "Medium"
    else:
        confidence_band = "Low"

    return {
        "success_probability": round(probability, 4),
        "prediction": prediction,
        "confidence_band": confidence_band,
    }