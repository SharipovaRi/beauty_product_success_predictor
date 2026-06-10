import pandas as pd
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_PATH = BASE_DIR / "data" / "raw" / "product_info.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "beauty_products_clean.csv"

# Function to clean text data by converting to lowercase and stripping whitespace
def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).lower().strip()

# Function to clean price data by removing currency symbols and converting to float
def clean_price(value):
    if pd.isna(value):
        return np.nan

    value = str(value)

    value = value.replace("$", "")
    value = value.replace(",", "")
    value = value.strip()

    try:
        return float(value)
    except:
        return np.nan

# Main function to load raw data, clean it, and save the cleaned data for feature engineering.
def main():

    df = pd.read_csv(RAW_PATH)

    print("Original Shape:", df.shape)
    # Select only relevant columns for modeling and drop unnecessary ones to reduce noise and improve model performance.
    keep_cols = [
        "product_id",
        "product_name",
        "brand_id",
        "brand_name",
        "loves_count",
        "rating",
        "reviews",
        "size",
        "variation_type",
        "variation_value",
        "variation_desc",
        "ingredients",
        "price_usd",
        "value_price_usd",
        "sale_price_usd",
        "limited_edition",
        "new",
        "online_only",
        "out_of_stock",
        "sephora_exclusive",
        "highlights",
        "primary_category",
        "secondary_category",
        "tertiary_category",
        "child_count",
        "child_max_price",
        "child_min_price"
    ]

    df = df[keep_cols].copy()
    # Clean text columns by converting to lowercase and stripping whitespace to ensure consistency and reduce noise in the data.
    text_cols = [
        "product_name",
        "brand_name",
        "size",
        "variation_type",
        "variation_value",
        "variation_desc",
        "ingredients",
        "highlights",
        "primary_category",
        "secondary_category",
        "tertiary_category"
    ]

    for col in text_cols:
        df[col] = df[col].apply(clean_text)

    # Clean price columns by removing currency symbols and converting to float for accurate numerical analysis and modeling.
    price_cols = [
        "price_usd",
        "value_price_usd",
        "sale_price_usd",
        "child_max_price",
        "child_min_price"
    ]

    for col in price_cols:
        df[col] = df[col].apply(clean_price)

    # Convert binary columns to integers (0 and 1) and fill missing values with 0, as these columns represent the presence or absence of certain product attributes.
    numeric_cols = [
        "loves_count",
        "rating",
        "reviews",
        "child_count"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce") # Convert to numeric, coercing errors to NaN for proper handling of non-numeric values.

    # Fill missing values for binary and numeric columns with appropriate defaults (0 for binary, median for numeric) to ensure the dataset is complete and ready for modeling.
    binary_cols = [
        "limited_edition",
        "new",
        "online_only",
        "out_of_stock",
        "sephora_exclusive"
    ]
    
    for col in binary_cols:
        df[col] = df[col].fillna(0).astype(int)

    df["reviews"] = df["reviews"].fillna(0)
    df["loves_count"] = df["loves_count"].fillna(0)

    df["sale_price_usd"] = df["sale_price_usd"].fillna(0)

    df["value_price_usd"] = df["value_price_usd"].fillna(
        df["price_usd"]
    )

    df["child_count"] = df["child_count"].fillna(0)

    df["child_max_price"] = df["child_max_price"].fillna(
        df["price_usd"]
    )

    df["child_min_price"] = df["child_min_price"].fillna(
        df["price_usd"]
    )

    # Drop rows with missing values in critical columns that are essential for modeling for reliability.
    df = df.dropna(
        subset=[
            "product_id",
            "product_name",
            "brand_name",
            "primary_category",
            "price_usd",
            "rating"
        ]
    )

    df = df[df["price_usd"] > 0]

    df = df[
        (df["rating"] >= 0)
        & (df["rating"] <= 5)
    ]

    # Calculate category medians for reviews and loves_count
    category_review_median = (
        df.groupby("primary_category")["reviews"]
        .transform("median")
    )

    category_love_median = (
        df.groupby("primary_category")["loves_count"]
        .transform("median")
    )

    df["success_label"] = (
        (df["rating"] >= 4.3)
        &
        (df["reviews"] >= category_review_median)
        &
        (df["loves_count"] >= category_love_median)
    ).astype(int)


    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nCleaning Complete")
    print("Final Shape:", df.shape)

    print("\nSuccess Label Distribution")
    print(df["success_label"].value_counts())

    print("\nSuccess Label Percentage")
    print(
        df["success_label"]
        .value_counts(normalize=True)
        .round(3)
    )

    print("\nSaved To:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()