import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Convert prediction results and product input into a business recommendation. 
def generate_launch_insight(prediction_result, product_input):
    probability = prediction_result["success_probability"]
    positives = prediction_result.get("top_positive_drivers", [])
    negatives = prediction_result.get("top_negative_drivers", [])
    # Top 3 positive and negative features.
    positive_features = [item["feature"] for item in positives[:3]]
    negative_features = [item["feature"] for item in negatives[:3]]

    if probability >= 0.7:
        launch_level = "Strong launch potential"

    elif probability >= 0.45:
        launch_level = "Moderate launch potential"

    else:
        launch_level = "High launch risk"

    prompt = f"""
    You are a beauty industry product strategy consultant.

    Product Information:
    Category: {product_input.primary_category}
    Price: {product_input.price_usd}

    Prediction Results:
    Success Probability: {probability}

    Top Positive Drivers:
    {positive_features}

    Top Negative Drivers:
    {negative_features}

    Write a concise business recommendation (3-5 sentences).

    Do not provide medical advice.
    Do not guarantee success.
    Focus on pricing, positioning, competition, branding, and product strategy.
    """

    try:
        response = model.generate_content(prompt)

        return response.text

    except Exception:

        return (
            f"{launch_level}. "
            f"Positive signals include {', '.join(positive_features)}. "
            f"Risk signals include {', '.join(negative_features)}."
        )

# Answer user's questions about the prediction. 
def answer_chatbot_question(question, context):
    """
    Answers user questions about a prediction.
    Supports both:
    1. direct prediction context
    2. prediction context with conversation history
    """

    prediction_context = context.get("prediction", context)
    conversation_history = context.get("conversation_history", [])

    prompt = f"""
    You are an AI Beauty Product Strategy Assistant.

    You help users understand machine learning predictions
    for beauty product launches.

    Prediction Context:
    {prediction_context}

    Previous Conversation:
    {conversation_history}

    Current User Question:
    {question}

    Rules:
    - Use the prediction context and previous conversation when relevant.
    - Answer the current user question directly.
    - Explain prediction drivers when useful.
    - Discuss pricing, positioning, branding, category competition, and ingredients.
    - Do not provide medical advice.
    - Do not guarantee product success.
    - Be concise, professional, and practical.
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print("Gemini chatbot failed:")
        print(e)

        return rule_based_answer(
            question,
            prediction_context
        )
    
# Fallback rule-based chatbot if Gemini is unavailable.
def rule_based_answer(question, context):
    """
    Fallback chatbot if Gemini is unavailable.
    """

    prediction_context = context.get("prediction", context)

    q = question.lower()

    probability = prediction_context.get(
        "success_probability",
        "unknown"
    )

    prediction = prediction_context.get(
        "prediction",
        "unknown"
    )

    confidence = prediction_context.get(
        "confidence_band",
        "unknown"
    )

    positives = prediction_context.get(
        "top_positive_drivers",
        []
    )

    negatives = prediction_context.get(
        "top_negative_drivers",
        []
    )

    positive_features = [
        item.get("feature", "")
        for item in positives[:3]
    ]

    negative_features = [
        item.get("feature", "")
        for item in negatives[:3]
    ]

    if "strategy" in q or "recommend" in q or "pricing" in q or "price" in q:
        return (
            f"For this product, focus on reducing the strongest risk drivers: "
            f"{', '.join(negative_features)}. "
            f"A better launch strategy could include clearer positioning, "
            f"stronger benefit-focused highlights, competitive pricing, and emphasizing positive drivers such as "
            f"{', '.join(positive_features)}."
        )

    if "why" in q:
        return (
            f"The model predicted '{prediction}' "
            f"with success probability {probability}. "
            f"The strongest positive drivers were "
            f"{', '.join(positive_features)}. "
            f"The strongest negative drivers were "
            f"{', '.join(negative_features)}."
        )

    if "improve" in q:
        return (
            f"Consider addressing the negative drivers: "
            f"{', '.join(negative_features)}. "
            f"Potential improvements may include pricing adjustments, "
            f"stronger positioning, or additional differentiation."
        )

    if "risk" in q:
        return (
            f"The primary risk signals identified by the model are: "
            f"{', '.join(negative_features)}."
        )

    return (
        f"Prediction: {prediction}. "
        f"Success probability: {probability}. "
        f"Confidence: {confidence}."
    )