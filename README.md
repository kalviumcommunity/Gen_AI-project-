# 🤖 LaughRx – The AI Roast Doctor

**LaughRx** is a humorous AI-powered chatbot that turns your symptoms into comedy — while giving you legit medical advice.  
The twist? You tell it your problems (like “I have a headache”), and it responds with:

- A **funny roast** about your life choices 
- **Actual health tips** using structured, AI-generated medical insights 

It's where WebMD meets stand-up comedy.

---

## Project Goals

This project explores the power of **Large Language Models (LLMs)** using the latest techniques like:

- Prompt engineering  
- Structured JSON outputs  
- Function calling for dynamic advice  
- Optional RAG (Retrieval-Augmented Generation) for factual answers  

All while keeping the experience fun and engaging.

---

##  Core Concepts Implemented

### 1. Prompting

**How we use it:**

- We use **custom system prompts** to define the bot’s personality.
- The prompt tells the LLM to:
  - Roast the user **in a playful tone**
  - Give **actual medical advice** only from verified sources or function output
  - Follow JSON structure for reliable parsing

**Example system prompt:**
> “You are a humorous AI doctor. First, lightly roast the user's symptoms. Then provide real medical advice in a JSON format. Stay funny but factual.”

This helps control the behavior of the AI and ensures consistent tone + accuracy.

---

### 2. Structured Output

**How we use it:**

- Every response is returned in a structured **JSON format** with 3 fields:
  - `roast` (string)
  - `diagnosis` (string)
  - `advice` (string)

This format ensures:
- Frontend can **reliably render** each section separately
- Easy integration with mobile apps or other clients
- Future compatibility with databases for storing advice logs

**Example Output:**
```json
{
  "roast": "Let me guess — you've had coffee, but not water today?",
  "diagnosis": "Likely dehydration or tension headache",
  "advice": "Drink water, reduce screen time, and rest. Consult a doctor if it persists."
}
