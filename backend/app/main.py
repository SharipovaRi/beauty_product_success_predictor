from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schemas import ProductInput, PredictionResponse
from backend.app.predict_service import predict_product, build_features_for_input
from backend.app.shap_service import explain_prediction


app = FastAPI(
    title="AI Beauty Product Success Predictor",
    version="1.0.0",
)

# Configure CORS to allow requests from the frontend application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint to verify API is running
@app.get("/")
def root():
    return {"message": "AI Beauty Product Success Predictor API"}

# Health check endpoint to monitor API status
@app.get("/health")
def health():
    return {"status": "healthy"}

# Endpoint to receive product data, generate prediction, and return results with explanations.
@app.post("/predict", response_model=PredictionResponse)
def predict(product: ProductInput):
    prediction_result = predict_product(product)

    X = build_features_for_input(product)

    positive_drivers, negative_drivers = explain_prediction(X)

    prediction_result["top_positive_drivers"] = positive_drivers
    prediction_result["top_negative_drivers"] = negative_drivers

    return prediction_result