"use client";

import { useState } from "react";

export default function Home() {
  const [productName, setProductName] = useState("");
  const [brandName, setBrandName] = useState("");
  const [category, setCategory] = useState("");
  const [price, setPrice] = useState("");

  return (
    <main className="min-h-screen bg-white p-8">
      <header className="flex items-center py-6">
        <div className="flex-1">
          <h1 className="text-xl font-bold">BeautyLaunch AI</h1>
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
            BeautyLaunch AI is a machine learning application that predicts
            whether a beauty product is likely to succeed based on historical
            Sephora product data. The system analyzes pricing, brand strength,
            product categories, ingredients, and market-positioning signals to
            estimate product success probability.
          </p>
          <div className="mt-6 grid gap-5 md:grid-cols-3">
            <div className="rounded-xl border-2 p-5">
              <h3 className="mb-2 font-semibold">ML Prediction</h3>
              <p className="text-sm text-gray-700">
                Predicts success probability using product features, pricing,
                category, brand, and ingredient signals.
              </p>
            </div>

            <div className="rounded-xl border-2 p-5">
              <h3 className="mb-2 font-semibold">Explainability</h3>
              <p className="text-sm text-gray-700">
                Shows positive and negative drivers that contributed most to the
                model prediction.
              </p>
            </div>

            <div className="rounded-xl border-2 p-5">
              <h3 className="mb-2 font-semibold">AI Strategy Insights</h3>
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

          <div className="grid gap-4">
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

            <input
              className="rounded border p-3"
              placeholder="Category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            />

            <input
              className="rounded border p-3"
              placeholder="Price (USD)"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          </div>

          <div className="flex justify-center">
            <button className="mt-6 rounded-2xl border-2 border-black bg-white px-8 py-4 font-semibold text-black shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-gray-500 hover:text-gray-500 hover:shadow-md">
              Submit Prediction
            </button>
          </div>
        </div>
      </section>

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

                <div>
                  <h3 className="font-semibold">Email</h3>
                  <p className="text-gray-700">
                    ritasharipova10@email.com
                  </p>
                </div>

                <div>
                  <h3 className="font-semibold">Location</h3>
                  <p className="text-gray-700">
                    Tampa/Orlando, Florida
                  </p>
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
                />

                <input
                  className="rounded-xl border p-3"
                  placeholder="Your Email"
                />

                <textarea
                  className="min-h-40 rounded-xl border p-3"
                  placeholder="Your Message"
                />
                <div className="flex justify-center">
                  <button className="mt-6 rounded-2xl border-2 border-black bg-white px-8 py-4 font-semibold text-black shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-gray-500 hover:text-gray-500 hover:shadow-md">
                    Send Message
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