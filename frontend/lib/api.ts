const API_BASE_URL = "http://localhost:8000";

/*
Calls FastAPI /predict endpoint
and returns prediction results.
*/
export async function predictProduct(
  productData: Record<string, unknown>
) {
  const response = await fetch(
    `${API_BASE_URL}/predict`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(productData),
    }
  );

  if (!response.ok) {
    throw new Error("Prediction request failed");
  }

  return response.json();
}

/*
Calls FastAPI /chat endpoint
and returns chatbot response.
*/
export async function askChatbot(
  question: string,
  predictionContext: Record<string, unknown>
) {
  const response = await fetch(
    `${API_BASE_URL}/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        prediction_context: predictionContext,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Chat request failed");
  }

  return response.json();
}
