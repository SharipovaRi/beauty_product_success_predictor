import pandas as pd
from backend.app.predict_service import pipeline

# Function to extract feature names from the preprocessor for SHAP explanations.
def get_feature_names():
    preprocessor = pipeline.named_steps["preprocessor"]

    feature_names = []

    for name, transformer, columns in preprocessor.transformers_:
        if name == "num":
            feature_names.extend(columns)

        elif name == "cat":
            cat_names = transformer.get_feature_names_out(columns)
            feature_names.extend(cat_names)

        elif name == "text":
            text_names = transformer.get_feature_names_out()
            feature_names.extend([f"text_{word}" for word in text_names])

    return feature_names

# Function to identify the top positive and negative drivers of the prediction.
def explain_prediction(X):
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    X_transformed = preprocessor.transform(X)
   
    # From sparsae matrix to array
    if hasattr(X_transformed, "toarray"):
        X_transformed = X_transformed.toarray()

    feature_names = get_feature_names()

    coefficients = model.coef_[0]
    feature_values = X_transformed[0]

    # Impact is calculated as the product of the feature value and its corresponding coefficient, which indicates how much each feature contributes to pushing the prediction towards success or failure.
    impacts = coefficients * feature_values

    explanation_df = pd.DataFrame(
        {
            "feature": feature_names,
            "impact": impacts,
        }
    )

    explanation_df = explanation_df[explanation_df["impact"] != 0]  # remove features with zero impact for clearer explanations

    positive_drivers = (
        explanation_df
        .sort_values("impact", ascending=False)
        .head(5)
        .round({"impact": 4})
        .to_dict(orient="records")
    )

    negative_drivers = (
        explanation_df
        .sort_values("impact", ascending=True)
        .head(5)
        .round({"impact": 4})
        .to_dict(orient="records")
    )

    return positive_drivers, negative_drivers