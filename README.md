# 🤖 LaughRx – The AI Roast Doctor

> "Because laughter *might* not cure everything, but at least you'll leave smiling."

---

## 🩺 Project Overview

**LaughRx** is an AI-powered chatbot that turns health symptom checks into stand-up comedy acts. Users share symptoms in plain English, and in return, the bot:

- 🔥 Roasts their life choices (yes, caffeine counts as a food group apparently)
- 💊 Delivers **real medical advice** with structured, accurate diagnoses
- 🧠 Uses LLMs, Function Calling, and optionally Retrieval-Augmented Generation (RAG)

Aimed at making self-diagnosis **fun, safe, and informative**, LaughRx is ideal for users seeking light-hearted clarity on minor symptoms.

---

## 🧠 How It Works

1. **User Input**:  
   “I have a headache and blurry vision.”

2. **System + User Prompting**:  
   The LLM is instructed to behave like a sarcastic doctor first, then offer legit medical advice.

3. **Function Calling**:  
   Calls `getMedicalAdvice(symptom)` to fetch accurate, structured health insights.

4. **Structured Output**:  
   Returns a roast, probable diagnosis, and first-aid level advice in clean JSON format.

5. **Optional RAG** (Extendable):  
   Uses LangChain to pull verified health data from sources like NHS, Mayo Clinic, or MedlinePlus for freshness and factual support.

---

## 🛠 Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | React.js / Vite / Tailwind (Chat UI) |
| Backend    | Node.js + Express.js              |
| AI Model   | OpenAI GPT-4 (with Function Calling) |
| Data       | Mock DB / JSON or RAG (LangChain) |
| Optional   | Whisper (voice input), Text-to-Speech, Roast Meter |

---

## 📦 API Sample Response

```json
{
  "roast": "Oh look, another human running on 3 hours of sleep and vibes.",
  "diagnosis": "Likely sleep deprivation or eye strain.",
  "advice": "Try reducing screen time, hydrate, and fix your sleep cycle."
}
