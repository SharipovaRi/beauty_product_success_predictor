import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = BASE_DIR / "data" / "processed" / "beauty_products_clean.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "beauty_products_features.csv"

# Popular beauty/skincare ingredients based on common product claims and consumer interest.
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

# Function to count the number of ingredients in the ingredient list
def count_ingredients(text):
    if pd.isna(text) or text == "":
        return 0

    ingredients = [
        ingredient.strip()
        for ingredient in str(text).split(",")
        if ingredient.strip()
    ]

    return len(ingredients)

# If ingredient exists in the ingredient list, return 1, else return 0
def contains_term(text, term):
    if pd.isna(text):
        return 0

    return int(term in str(text).lower())

# Function to categorize price into tiers
def make_price_tier(price):
    if price < 20:
        return "budget"
    elif price < 50:
        return "mid_range"
    elif price < 100:
        return "premium"
    else:
        return "luxury"


def main():
    df = pd.read_csv(INPUT_PATH)

    print("Input shape:", df.shape)

    # Count ingredients to see formula complexity 
    df["ingredient_count"] = df["ingredients"].apply(count_ingredients)
    
    # Count of marketing claims to see marketing strength
    df["highlight_count"] = (
        df["highlights"]
        .fillna("")
        .apply(lambda x: len([item.strip() for item in str(x).split(",") if item.strip()]))
    )

    # Length of product name, ingredients text, and highlights text.
    # Richer product descriptions may capture stronger product positioning.
    df["product_name_length"] = df["product_name"].fillna("").apply(len)
    df["ingredients_text_length"] = df["ingredients"].fillna("").apply(len)
    df["highlights_text_length"] = df["highlights"].fillna("").apply(len)

    # Price features
    df["price_tier"] = df["price_usd"].apply(make_price_tier)

    df["has_sale_price"] = (df["sale_price_usd"] > 0).astype(int)

    df["discount_amount"] = np.where(
        df["sale_price_usd"] > 0,
        df["price_usd"] - df["sale_price_usd"],
        0,
    )

    df["discount_pct"] = np.where(
        (df["sale_price_usd"] > 0) & (df["price_usd"] > 0),
        df["discount_amount"] / df["price_usd"],
        0,
    )

    df["value_price_gap"] = df["value_price_usd"] - df["price_usd"]

    # Ingredient flags
    for ingredient in POPULAR_INGREDIENTS:
        col_name = "contains_" + ingredient.replace(" ", "_")
        df[col_name] = df["ingredients"].apply(lambda x: contains_term(x, ingredient))

    ingredient_flag_cols = [
        col for col in df.columns
        if col.startswith("contains_")
    ]

    # To capture the presence of popular ingredients, which can be a strong signal of product success in skincare category.
    df["popular_ingredient_count"] = df[ingredient_flag_cols].sum(axis=1)

    # Brand-level aggregate features
    brand_stats = (
        df.groupby("brand_name")
        .agg(
            brand_product_count=("product_id", "count"),
            brand_avg_price=("price_usd", "mean"),
            brand_success_rate=("success_label", "mean"),
            brand_limited_edition_rate=("limited_edition", "mean"),
            brand_sephora_exclusive_rate=("sephora_exclusive", "mean"),
        )
        .reset_index()
    )

    # Category-level aggregate features
    category_stats = (
        df.groupby("primary_category")
        .agg(
            category_product_count=("product_id", "count"),
            category_avg_price=("price_usd", "mean"),
            category_success_rate=("success_label", "mean"),
            category_limited_edition_rate=("limited_edition", "mean"),
            category_sephora_exclusive_rate=("sephora_exclusive", "mean"),
        )
        .reset_index()
    )

    # Secondary category aggregate features
    secondary_category_stats = (
        df.groupby("secondary_category")
        .agg(
            secondary_category_product_count=("product_id", "count"),
            secondary_category_avg_price=("price_usd", "mean"),
            secondary_category_success_rate=("success_label", "mean"),
        )
        .reset_index()
    )

    # Merge aggregate features back to main dataframe
    df = df.merge(brand_stats, on="brand_name", how="left")
    df = df.merge(category_stats, on="primary_category", how="left")
    df = df.merge(secondary_category_stats, on="secondary_category", how="left")

    # Relative market-positioning features
    df["price_vs_category_avg"] = df["price_usd"] / df["category_avg_price"]
    df["price_vs_brand_avg"] = df["price_usd"] / df["brand_avg_price"]

    # Category saturation features to capture how crowded the category is, which can impact product success.
    df["category_saturation_score"] = (
        df["category_product_count"] / df["category_product_count"].max()
    )
    # Secondary category saturation score to capture how crowded the secondary category is, which can impact product success.
    df["secondary_category_saturation_score"] = (
        df["secondary_category_product_count"]
        / df["secondary_category_product_count"].max()
    )

    # Product variation features (Example, shows if the product has different shades or not)
    df["has_variation"] = (
        df["variation_type"].fillna("").str.len() > 0
    ).astype(int)

    # Size information exists or not. 
    df["has_size"] = (
        df["size"].fillna("").str.len() > 0
    ).astype(int)

    # Product family exists or not.
    df["has_child_products"] = (
        df["child_count"] > 0
    ).astype(int)

    df["child_price_range"] = df["child_max_price"] - df["child_min_price"]

    # Combined text for TF-IDF model input
    df["product_text"] = (
        df["product_name"].fillna("") + " " +
        df["brand_name"].fillna("") + " " +
        df["primary_category"].fillna("") + " " +
        df["secondary_category"].fillna("") + " " +
        df["tertiary_category"].fillna("") + " " +
        df["ingredients"].fillna("") + " " +
        df["highlights"].fillna("") + " " +
        df["variation_desc"].fillna("")
    )

    # Replace infinite values caused by division
    df = df.replace([np.inf, -np.inf], np.nan)

    # Fill numeric missing values created during feature engineering with median values (more robust to outliers than mean).
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())


    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(OUTPUT_PATH, index=False)

    print("Feature engineering complete.")
    print("Output shape:", df.shape)
    print("Saved to:", OUTPUT_PATH)

    print("\nCreated feature columns:")
    created_cols = [
        "ingredient_count",
        "highlight_count",
        "price_tier",
        "popular_ingredient_count",
        "brand_product_count",
        "brand_success_rate",
        "category_product_count",
        "category_success_rate",
        "price_vs_category_avg",
        "category_saturation_score",
        "product_text",
    ]

    for col in created_cols:
        print("-", col)


if __name__ == "__main__":
    main()