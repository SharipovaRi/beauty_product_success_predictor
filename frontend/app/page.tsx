"use client";
import { predictProduct, askChatbot} from "../lib/api";
import { useState } from "react";
import { Mail, MapPin } from "lucide-react";

export default function Home() {
  const [productName, setProductName] = useState("");
  const [brandName, setBrandName] = useState("");
  const [category, setCategory] = useState("");
  const [price, setPrice] = useState("");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState("");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [history, setHistory] = useState<
  {
    productName: string;
    brandName: string;
    probability: number;
    prediction: string;
  }[]
  >([]);
  /* Categories are based on the dataset */
  const categories = [
  "Skincare",
  "Makeup",
  "Hair",
  "Fragrance",
  "Bath & Body",
  "Tools & Brushes",
  ];
  const [limitedEdition, setLimitedEdition] = useState(false);
  const [sephoraExclusive, setSephoraExclusive] = useState(false);
  const [contactName, setContactName] = useState("");
  const [contactEmail, setContactEmail] = useState("");
  const [contactMessage, setContactMessage] = useState("");
  const [sendingMessage, setSendingMessage] = useState(false);

  type Driver = {
  feature: string;
  impact: number;
  };

  type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  };
  
  async function handlePredict() {
  if (!productName || !brandName || !category || !price) {
    alert("Please fill in product name, brand name, category, and price.");
    return;
    }

    if (Number(price) <= 0) {
      alert("Please enter a valid price.");
      return;
}
  setLoading(true);

  const payload = {
    product_name: productName,
    brand_name: brandName,
    primary_category: category,
    secondary_category: "",
    tertiary_category: "",
    variation_type: "",
    price_usd: Number(price),
    value_price_usd: Number(price),
    sale_price_usd: 0,
    new: 1,
    online_only: 0,
    out_of_stock: 0,
    limited_edition: limitedEdition ? 1 : 0,
    sephora_exclusive: sephoraExclusive ? 1 : 0,
    size: "",
    variation_desc: "",
    ingredients: "niacinamide, zinc, glycerin, panthenol",
    highlights: "brightening, oil-control, fragrance-free",
  };

  try {
    const data = await predictProduct(payload);
    setResult(data);
    setHistory((prev) => [
  {
    productName,
    brandName,
    probability: data.success_probability,
    prediction: data.prediction,
  },
  ...prev.slice(0, 4),
]);
  } catch (error) {
    console.error(error);
    alert("Prediction failed. Make sure FastAPI is running.");
  } finally {
    setLoading(false);
  }
}

async function handleAskChatbot() {
  if (!result || !question.trim()) return;

  const userMessage: ChatMessage = {
    role: "user",
    content: question,
  };

  setChatMessages((prev) => [...prev, userMessage]);
  setQuestion("");
  setChatLoading(true);

  try {
    const data = await askChatbot(question, result);

    const assistantMessage: ChatMessage = {
      role: "assistant",
      content: data.answer,
    };

    setChatMessages((prev) => [...prev, assistantMessage]);
  } catch (error) {
    console.error(error);

    setChatMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "Sorry, I could not generate a response. Please try again.",
      },
    ]);
  } finally {
    setChatLoading(false);
  }
}

async function handleContactSubmit() {

  if (
    !contactName ||
    !contactEmail ||
    !contactMessage
  ) {
    alert("Please fill out all fields.");
    return;
  }

  setSendingMessage(true);

  try {

    const response = await fetch(
      "/api/contact",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: contactName,
          email: contactEmail,
          message: contactMessage,
        }),
      }
    );

    if (!response.ok) {
      throw new Error();
    }

    alert("Message sent successfully!");

    setContactName("");
    setContactEmail("");
    setContactMessage("");

  } catch {

    alert(
      "Failed to send message."
    );

  } finally {

    setSendingMessage(false);

  }
}

  return (
    <main className="min-h-screen bg-white p-8">
      <header className="sticky top-0 z-50 flex items-center bg-transparent py-6 ">
        <div className="flex-1 ">
          <h1 className="text-xl font-bold">BeautyLaunch </h1>
        </div>

        <nav className="flex items-center gap-8 rounded-full border border-gray-200 bg-white px-8 py-3 shadow-sm">
          <a href="#home" className="text-sm font-semibold hover:text-gray-500">
            Home
          </a>

          <a href="#predict" className="text-sm font-semibold hover:text-gray-500">
            Predict
          </a>

          <a href="#contact" className="text-sm font-semibold hover:text-gray-500">
            Contact
          </a>
        </nav>

        <div className="flex-1"></div>
      </header>

      <section id="home" className="mx-auto max-w-5xl pt-10">
        <div className="rounded-2xl text-center p-8 ">
          <h1 className="text-5xl font-bold">
            Predict Beauty Product Success Before Launch
          </h1>

          <p className="mt-4 text-gray-700">
            <b>BeautyLaunch</b> is a machine learning application that predicts
            whether a beauty product is likely to succeed based on historical
            Sephora product data. The system analyzes pricing, brand strength,
            product categories, ingredients, and market-positioning signals to
            estimate product success probability.
          </p>
          <div className="mt-6 grid gap-5 md:grid-cols-3 ">
            <div className="rounded-xl border-2 p-5 shadow-md border-white hover:border-gray-300">
              <h3 className="mb-2 font-semibold text-red-700">ML Prediction</h3>
              <p className="text-sm text-gray-700">
                Predicts success probability using product features, pricing,
                category, brand, and ingredient signals.
              </p>
            </div>

            <div className="rounded-xl border-2 p-5 shadow-md border-white hover:border-gray-300">
              <h3 className="mb-2 font-semibold text-red-700">Explainability</h3>
              <p className="text-sm text-gray-700">
                Shows positive and negative drivers that contributed most to the
                model prediction.
              </p>
            </div>

            <div className="rounded-xl border-2 p-5 shadow-md border-white hover:border-gray-300">
              <h3 className="mb-2 font-semibold text-red-700">AI Strategy Insights</h3>
              <p className="text-sm text-gray-700">
                Uses AI to translate model results into business-oriented launch
                recommendations.
              </p>
            </div>
          </div>
        </div>
      </section>  

      <section id="predict" className="mx-auto max-w-5xl pt-10">
        <div className="rounded-2xl text-center bg-white p-8 shadow-md">
          <h2 className="mb-4 text-3xl font-semibold">Predict Product Success</h2>

          <p className="mb-6 text-gray-700">
            Enter the details of your beauty product below to get a success prediction.
          </p>

          <div className="grid gap-4 p-10 md:grid-cols-2">
            <input
              className="rounded border p-3"
              placeholder="Product Name"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
            />

            <input
              className="rounded border p-3"
              placeholder="Brand Name"
              value={brandName}
              onChange={(e) => setBrandName(e.target.value)}
            />

            <select
              className="rounded border p-3 "
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              <option value="">
                Select Category
              </option>

              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>

            <input
              className="rounded border p-3"
              placeholder="Price (USD)"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          
          
          <div className="flex gap-8">

            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={limitedEdition}
                onChange={(e) =>
                  setLimitedEdition(e.target.checked)
                }
              />

              <span>Limited Edition</span>
            </label>

            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={sephoraExclusive}
                onChange={(e) =>
                  setSephoraExclusive(e.target.checked)
                }
              />

              <span>Sephora Exclusive</span>
            </label>

          </div>
          </div>


          <div className="flex justify-center">
            <button
              onClick={handlePredict}
              className="mt-6 rounded-4xl border-2 border-black bg-white px-6 py-2 font-semibold text-black shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-gray-500 hover:text-gray-500 hover:shadow-md"
            >
              {loading ? "Analyzing..." : "Predict Success"}
            </button>
          </div>
        </div>
      </section>

      {result && (
  <section className="mx-auto mt-10 max-w-5xl">
    <div className="rounded-2xl bg-white p-8 shadow-md">

      <h2 className="mb-8 text-center text-3xl font-bold">
        Prediction Results
      </h2>

      {/* Summary Cards */}
      <div className="mb-8 grid gap-4 md:grid-cols-3">

        <div className="rounded-xl border p-5 text-center">
          <p className="text-sm text-gray-500">
            Success Probability
          </p>

          <p className="mt-2 text-3xl font-bold">
            {Math.round(Number(result.success_probability) * 100)}%
          </p>
        </div>

        <div className="rounded-xl border p-5 text-center">
          <p className="text-sm text-gray-500">
            Prediction
          </p>

          <p className="mt-2 text-3xl font-bold">
            {String(result.prediction)}
          </p>
        </div>

        <div className="rounded-xl border p-5 text-center">
          <p className="text-sm text-gray-500">
            Confidence
          </p>

          <p className="mt-2 text-3xl font-bold">
            {String(result.confidence_band)}
          </p>
        </div>

      </div>

      {/* Drivers */}
      <div className="grid gap-8 md:grid-cols-2">

        <div className="rounded-xl border p-5">
          <h3 className="mb-4 text-xl font-semibold">
            Positive Drivers
          </h3>

          <p className="mb-4 text-xs italic text-gray-500">
            Relative impact score (not a percentage).
          </p>

          {(result.top_positive_drivers as Driver[]).map((driver) => (
            <div key={driver.feature} className="mb-4">
            <div className="mb-1 flex justify-between text-sm">
              <span className="font-medium">
                {driver.feature}
              </span>

              <span className="text-gray-600">
                {driver.impact.toFixed(3)}
              </span>
            </div>

            <div className="h-2 rounded-full bg-gray-100">
              <div
                className="h-2 rounded-full bg-black"
                style={{
                  width: `${Math.min(Math.abs(driver.impact) * 80, 100)}%`,
                }}
              />
            </div>
          </div>
          ))}
        </div>

        <div className="rounded-xl border p-5">
          <h3 className="mb-4 text-xl font-semibold">
            Negative Drivers
          </h3>
          
          <p className="mb-4 text-xs italic text-gray-500">
            Relative impact score (not a percentage).
          </p>

          {(result.top_negative_drivers as Driver[]).map((driver) => (
            <div key={driver.feature} className="mb-4">
              <div className="mb-1 flex justify-between text-sm">
                <span className="font-medium">
                  {driver.feature}
                </span>

                <span className="text-gray-600">
                  {driver.impact.toFixed(3)}
                </span>
              </div>

              <div className="h-2 rounded-full bg-gray-100">
                <div
                  className="h-2 rounded-full bg-black"
                  style={{
                    width: `${Math.min(Math.abs(driver.impact) * 80, 100)}%`,
                  }}
                />  
              </div>
            </div>
          ))}
        </div>

      </div>

      {/* Gemini Insight */}
      <div className="mt-8 rounded-xl border p-5">

        <h3 className="mb-3 text-xl font-semibold">
          AI Launch Insight
        </h3>

        <p className="whitespace-pre-line text-gray-700">
          {String(result.ai_launch_insight)}
        </p>

      </div>

    </div>
  </section>
)}

{result && (
  <section className="mx-auto mt-10 max-w-5xl">
    <div className="rounded-2xl bg-white p-8 shadow-md">
      <h2 className="mb-4 text-center text-3xl font-bold">
        Ask BeautyLaunch
      </h2>

      <p className="mb-6 text-center text-gray-700">
        Ask questions about pricing, positioning, risks, ingredients, or launch strategy.
      </p>

      <p className="mb-6 text-left text-gray-700">
       <b className="text-red-700">DISCLAIMER</b>: The system does not provide medical, dermatology, allergy, or cosmetic safety advice. Model outputs should be interpreted as business/product strategy estimates, not guaranteed product outcomes.
       </p>

      <div className="mx-auto max-w-3xl rounded-2xl border bg-gray-50 p-4">
        <div className="mb-4 max-h-96 overflow-y-auto space-y-4 pr-2">
    
          {chatMessages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-6 ${
                  message.role === "user"
                    ? "bg-black text-white"
                    : "border bg-white text-gray-700"
                }`}
              >
                <p className="whitespace-pre-line">{message.content}</p>
              </div>
            </div>
          ))}

          {chatLoading && (
            <div className="flex justify-start">
              <div className="rounded-2xl border bg-white px-4 py-3 text-sm text-gray-500">
                BeautyLaunch AI is thinking...
              </div>
            </div>
          )}
        </div>

        <div className="flex gap-3">
          <input
            className="flex-1 rounded-xl border bg-white p-3"
            placeholder="Ask about risks, pricing, or improvement strategy..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleAskChatbot();
              }
            }}
          />

          <button
            onClick={handleAskChatbot}
            disabled={chatLoading}
            className="rounded-4xl border-2 border-black bg-white px-10 py-2 font-semibold text-black shadow-sm transition hover:-translate-y-0.5 hover:border-gray-500 hover:text-gray-500 hover:shadow-md disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  </section>
)}

{history.length > 0 && (
  <section className="mx-auto mt-10 max-w-5xl">
    <div className="rounded-2xl bg-white p-8 shadow-md">
      <h2 className="mb-6 text-center text-3xl font-bold">
        Recent Predictions
      </h2>

      <div className="grid gap-4">
        {history.map((item, index) => (
          <div
            key={`${item.productName}-${index}`}
            className="flex items-center justify-between rounded-xl border p-4"
          >
            <div>
              <h3 className="font-semibold">{item.productName}</h3>
              <p className="text-sm text-gray-600">{item.brandName}</p>
            </div>

            <div className="text-right">
              <p className="font-semibold">
                {Math.round(item.probability * 100)}%
              </p>
              <p className="text-sm text-gray-600">{item.prediction}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
)}
      <section id="contact" className="mx-auto mt-24 max-w-5xl pb-16">
          <h2 className="mb-10 text-center text-3xl font-bold">
            Get In Touch 
          </h2>
          <div className="grid gap-10 md:grid-cols-2">

            {/* Left Side */}
            <div className="border-gray-200 pr-0 text-center md:border-r-2 md:pr-10">

              <h2 className="mb-6 text-2xl font-bold">
                Contact Information
              </h2>

              <div className="grid gap-4 text-left">

                <div className="flex items-start gap-3">
                  <Mail size={20} className="mt-1 text-gray-600" />

                  <div>
                    <h3 className="font-semibold">Email</h3>
                    <p className="text-gray-700">
                      ritasharipova10@email.com
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <MapPin size={20} className="mt-1 text-gray-600" />

                  <div>
                    <h3 className="font-semibold">Location</h3>
                    <p className="text-gray-700">
                      Tampa/Orlando, Florida
                    </p>
                  </div>
                </div>

              </div>
            </div>

            {/* Right Side */}
            <div className="text-center">

              <h2 className="mb-6 text-2xl font-bold">
                Submit a Message
              </h2>

              <div className="grid gap-4">

                <input
                  className="rounded-xl border p-3"
                  placeholder="Your Name"
                  value={contactName}
                  onChange={(e) =>
                    setContactName(e.target.value)
                  }
                />

                <input
                  className="rounded-xl border p-3"
                  placeholder="Your Email"
                  value={contactEmail}
                  onChange={(e) =>
                    setContactEmail(e.target.value)
                  }
                />

                <textarea
                  className="min-h-40 rounded-xl border p-3"
                  placeholder="Your Message"
                  value={contactMessage}
                  onChange={(e) =>
                    setContactMessage(e.target.value)
                  }
                />

                <div className="flex justify-center">
                  <button 
                    onClick={handleContactSubmit}
                    disabled={sendingMessage}
                    className="mt-6 rounded-4xl border-2 border-black bg-white px-6 py-2 font-semibold text-black shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-gray-500 hover:text-gray-500 hover:shadow-md"
                  >
                    {sendingMessage
                      ? "Sending..."
                      : "Send Message"}
                  </button>
                </div>
              </div>

            </div>

        </div>
      </section>
      <footer className="mt-24 border-t border-gray-200 py-8">
        <div className="mx-auto max-w-5xl text-left text-sm text-gray-700">
          <p>
            © 2026 Rita Sharipova. All rights reserved.
          </p>
        </div>
      </footer>
    </main>
  );
}