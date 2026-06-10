import json
import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import cross_validate, train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "processed" / "beauty_products_features.csv"
MODEL_PATH = BASE_DIR / "models" / "product_success_pipeline.pkl"
COMPARISON_PATH = BASE_DIR / "reports" / "model_comparison.json"
METRICS_PATH = BASE_DIR / "reports" / "model_metrics.json"
REPORT_PATH = BASE_DIR / "reports" / "classification_report.txt"

# Function to extract features and target variable from the dataset, and identify numeric, categorical, and text features for modeling.
def get_features(df):
    target = "success_label"
    numeric_features = [
        "price_usd",
        "value_price_usd",
        "sale_price_usd",
        "limited_edition",
        "new",
        "online_only",
        "out_of_stock",
        "sephora_exclusive",
        "child_count",
        "child_max_price",
        "child_min_price",
        "ingredient_count",
        "highlight_count",
        "product_name_length",
        "ingredients_text_length",
        "highlights_text_length",
        "has_sale_price",
        "discount_amount",
        "discount_pct",
        "value_price_gap",
        "popular_ingredient_count",
        "brand_product_count",
        "brand_avg_price",
        "brand_success_rate",
        "brand_limited_edition_rate",
        "brand_sephora_exclusive_rate",
        "category_product_count",
        "category_avg_price",
        "category_success_rate",
        "category_limited_edition_rate",
        "category_sephora_exclusive_rate",
        "secondary_category_product_count",
        "secondary_category_avg_price",
        "secondary_category_success_rate",
        "price_vs_category_avg",
        "price_vs_brand_avg",
        "category_saturation_score",
        "secondary_category_saturation_score",
        "has_variation",
        "has_size",
        "has_child_products",
        "child_price_range",
    ]

    ingredient_features = [
        col for col in df.columns if col.startswith("contains_")
    ]

    numeric_features = numeric_features + ingredient_features
    numeric_features = [col for col in numeric_features if col in df.columns]

    categorical_features = [
        "brand_name",
        "primary_category",
        "secondary_category",
        "tertiary_category",
        "price_tier",
        "variation_type",
    ]

    categorical_features = [
        col for col in categorical_features if col in df.columns
    ]

    text_feature = "product_text"

    feature_columns = numeric_features + categorical_features + [text_feature]

    # Ensure all feature columns exist in the dataframe, and fill missing values appropriately (0 for binary, median for numeric, "unknown" for categorical) to prepare the dataset for modeling.
    X = df[feature_columns].copy()
    y = df[target].copy()

    X[text_feature] = X[text_feature].fillna("")

    for col in categorical_features:
        X[col] = X[col].fillna("unknown")

    for col in numeric_features:
        X[col] = X[col].fillna(X[col].median())

    return X, y, numeric_features, categorical_features, text_feature, feature_columns

# Build a machine learning pipeline that includes preprocessing steps for numeric, categorical, and text features, followed by the specified model. This pipeline will be used for training and evaluation.
def build_pipeline(model, numeric_features, categorical_features, text_feature):
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                numeric_features,
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
            (
                "text",
                TfidfVectorizer(
                    max_features=700,
                    ngram_range=(1, 2),
                    min_df=2,
                ),
                text_feature,
            ),
        ]
    )
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    return pipeline


def main():
    df = pd.read_csv(DATA_PATH)

    print("Dataset shape:", df.shape)
    X, y, numeric_features, categorical_features, text_feature, feature_columns = get_features(df)

    # Define a set of models to compare, including Logistic Regression, Random Forest, and XGBoost, with appropriate hyperparameters for each model to ensure a fair comparison.
    models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    ),

    "XGBoost": XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        eval_metric="logloss",
        random_state=42,
    ),
}
    # Define scoring metrics for model evaluation, including accuracy, precision, recall, F1 score, and ROC AUC, to comprehensively assess the performance of each model during cross-validation.
    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc",
    }

    comparison_results = {}

    for model_name, model in models.items():
        print(f"\nComparing model: {model_name}")

        pipeline = build_pipeline(
            model=model,
            numeric_features=numeric_features,
            categorical_features=categorical_features,
            text_feature=text_feature,
        )
        # Perform cross-validation for the current model and compute the average of each scoring metric across the folds to evaluate the model's performance.
        cv_results = cross_validate(
            pipeline,
            X,
            y,
            cv=5,
            scoring=scoring,
            n_jobs=-1,
            return_train_score=False,
        )

        comparison_results[model_name] = {
            "accuracy": round(float(cv_results["test_accuracy"].mean()), 3),
            "precision": round(float(cv_results["test_precision"].mean()), 3),
            "recall": round(float(cv_results["test_recall"].mean()), 3),
            "f1": round(float(cv_results["test_f1"].mean()), 3),
            "roc_auc": round(float(cv_results["test_roc_auc"].mean()), 3),
        }

        print(comparison_results[model_name])

    # The best model is based on the highest F1 score from the cross-validation results and save results.
    best_model_name = max(
        comparison_results,
        key=lambda name: comparison_results[name]["f1"],
    )
    comparison_results["best_model_by_f1"] = best_model_name
    print("\nBest model by F1:", best_model_name)

    COMPARISON_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(COMPARISON_PATH, "w") as f:
        json.dump(comparison_results, f, indent=4)

    best_model = models[best_model_name]

    # Build the final pipeline with the best model and train it on the entire training dataset, then evaluate its performance on a held-out test set and save the final metrics, classification report, confusion matrix, and the trained model for future use.
    final_pipeline = build_pipeline(
        model=best_model,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        text_feature=text_feature,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    final_pipeline.fit(X_train, y_train)

    y_pred = final_pipeline.predict(X_test)
    y_prob = final_pipeline.predict_proba(X_test)[:, 1]

    final_metrics = {
    "selected_model": best_model_name,
    "accuracy": round(accuracy_score(y_test, y_pred), 3),
    "precision": round(precision_score(y_test, y_pred), 3),
    "recall": round(recall_score(y_test, y_pred), 3),
    "f1": round(f1_score(y_test, y_pred), 3),
    "roc_auc": round(roc_auc_score(y_test, y_prob), 3),
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(METRICS_PATH, "w") as f:
        json.dump(final_metrics, f, indent=4)

    with open(REPORT_PATH, "w") as f:
        f.write(f"Selected Model: {best_model_name}\n\n")
        f.write(classification_report(y_test, y_pred))
        f.write("\n\nConfusion Matrix:\n")
        f.write(str(confusion_matrix(y_test, y_pred)))

    joblib.dump(
        {
            "pipeline": final_pipeline,
            "selected_model": best_model_name,
            "numeric_features": numeric_features,
            "categorical_features": categorical_features,
            "text_feature": text_feature,
            "feature_columns": feature_columns,
        },
        MODEL_PATH,
    )

    print("\nFinal model training complete.")
    print("Selected model:", best_model_name)
    print("Saved model to:", MODEL_PATH)
    print("Saved comparison to:", COMPARISON_PATH)
    print("Saved metrics to:", METRICS_PATH)

    print("\nFinal Metrics:")
    print(final_metrics)


if __name__ == "__main__":
    main()