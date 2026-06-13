from pydantic import BaseModel
from typing import List, Optional

# Input schema for incoming requests to the API.
class ProductInput(BaseModel):
    product_name: Optional[str] = ""
    brand_name: str
    primary_category: str
    secondary_category: Optional[str] = ""
    tertiary_category: Optional[str] = ""
    variation_type: Optional[str] = ""
    price_usd: float
    value_price_usd: Optional[float] = None
    sale_price_usd: Optional[float] = 0
    limited_edition: int = 0
    new: int = 1
    online_only: int = 0
    out_of_stock: int = 0
    sephora_exclusive: int = 0
    size: Optional[str] = ""
    variation_desc: Optional[str] = ""
    ingredients: str
    highlights: Optional[str] = ""

# Driver schema to represent the key factors influencing the prediction.
class Driver(BaseModel):
    feature: str
    impact: float

# Output schema for the API response.
class PredictionResponse(BaseModel):
    success_probability: float
    prediction: str
    confidence_band: str
    top_positive_drivers: List[Driver]
    top_negative_drivers: List[Driver]    
    ai_launch_insight: str

class ChatRequest(BaseModel):
    question: str
    prediction_context: dict

class ChatResponse(BaseModel):
    answer: str