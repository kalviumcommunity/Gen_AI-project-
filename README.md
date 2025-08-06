# Gen_AI-project-
# 🤖 LaughRx – The AI Roast Doctor

 “Where your symptoms meet sarcasm, and you leave healthier AND humbled.”

**LaughRx** is a quirky, intelligent AI chatbot that turns everyday health complaints into stand-up comedy followed by real medical advice. It's like talking to a doctor… if the doctor were a roast comedian with a medical degree.

---

##  Features

-  Hilarious roast responses for your lifestyle choices
-  Accurate medical advice using Function Calling
-  Optional RAG (Retrieval-Augmented Generation) from verified sources
-  Friendly chat UI for web or mobile
-  Safe and informative first-aid-level symptom checker

---

##  Example

**User:** 
> "I feel tired all day and can't focus."

**LaughRx:**  
> “Wow, sounds like someone tried to survive on 4 hours of sleep and bad decisions again. Classic.”  
> **Diagnosis:** Fatigue (Possibly due to sleep deprivation)  
> **Advice:** Try regular sleep cycles, hydration, and screen detox.

---

## 🛠️ Tech Stack

| Layer       | Technology                    |
|-------------|-------------------------------|
| Frontend    | React.js OR HTML/CSS          |
| Backend     | Node.js + Express             |
| AI Engine   | OpenAI GPT-4 (Function Calling) |
| Data Source | Mock JSON / Medical APIs      |
| Optional    | LangChain (RAG), Whisper (STT) |

---

## 🔧 How It Works

1. **User Input**: Describes symptoms in plain English.
2. **AI Prompt**: Injects humor and context into the request.
3. **Function Calling**: Calls `getMedicalAdvice(symptom)` to fetch real advice.
4. **Optional RAG**: Pulls updated tips from sources like NHS or MedlinePlus.
5. **Structured Output**: Returns a roast + real diagnosis + treatment advice.


