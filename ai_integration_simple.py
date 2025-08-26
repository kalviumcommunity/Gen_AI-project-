"""
LaughRx - Simple AI Integration Test
===================================

This is a simplified version to test AI integration quickly.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

class LaughRxAISimple:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Sampling config
        # Top P (nucleus sampling) and Top K
        try:
            top_p_env = float(os.getenv("TOP_P", "0.9"))
            self.top_p = max(0.0, min(1.0, top_p_env))
            if self.top_p == 0.0:
                self.top_p = 0.01
        except Exception:
            self.top_p = 0.9
        try:
            top_k_env = int(os.getenv("TOP_K", "40"))
            # Clamp to non-negative; 0 disables top-k in many SDKs
            self.top_k = max(0, top_k_env)
        except Exception:
            self.top_k = 40

        # Default stop sequences from env (comma-separated)
        raw_stops = os.getenv("STOP_SEQUENCES", "")
        if raw_stops.strip():
            self.stop_sequences_default = [s.strip() for s in raw_stops.split(",") if s.strip()]
        else:
            self.stop_sequences_default = []
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        print(f"🎯 Generation top_p set to: {self.top_p}, top_k set to: {self.top_k}")
        if self.stop_sequences_default:
            print(f"⛔ Stop sequences set: {self.stop_sequences_default}")
        
        # LaughRx system prompt
        self.system_prompt = """You are LaughRx, a humorous AI doctor with a unique personality:

PERSONALITY TRAITS:
- You're witty and playful, but never mean-spirited
- You love to gently roast people's lifestyle choices
- You're medically knowledgeable and responsible
- You balance humor with genuine care for health

YOUR RESPONSE STRUCTURE:
1. Start with a light, funny roast about their symptoms or lifestyle
2. Provide a possible diagnosis or explanation
3. Give practical, helpful medical advice
4. Always remind them to consult a real doctor for serious concerns

TONE GUIDELINES:
- Keep roasts playful, not offensive
- Be encouraging despite the humor
- Use casual, friendly language
- Always include medical disclaimers for safety

Example response format:
🎭 ROAST: [Funny observation about their situation]
🔍 DIAGNOSIS: [Possible medical explanation]
💡 ADVICE: [Practical health advice]
⚠️ DISCLAIMER: Always consult a healthcare professional for persistent or serious symptoms."""
    
    def generate_response(self, symptoms: str, dynamic_options: dict | None = None) -> dict:
        """
        Generate AI response for symptoms with optional dynamic prompting.
        dynamic_options keys (all optional):
          - system_override: str
          - tone: str
          - persona: str
          - language: str
          - extra_instructions: str
          - user_context: dict
          - constraints: list[str]
          - examples: list[dict] where each dict can have keys like {"user": str, "assistant": str}
        """
        try:
            dynamic_options = dynamic_options or {}

            # Choose system prompt (override if provided)
            system_prompt = dynamic_options.get("system_override") or self.system_prompt

            # Build dynamic context block
            dynamic_lines = []
            tone = dynamic_options.get("tone")
            persona = dynamic_options.get("persona")
            language = dynamic_options.get("language")
            extra_instructions = dynamic_options.get("extra_instructions")
            user_context = dynamic_options.get("user_context") or {}
            constraints = dynamic_options.get("constraints") or []
            examples = dynamic_options.get("examples") or []

            if tone:
                dynamic_lines.append(f"- Desired tone: {tone}")
            if persona:
                dynamic_lines.append(f"- Adopt this persona: {persona}")
            if language:
                dynamic_lines.append(f"- Respond in language: {language}")
            if user_context and isinstance(user_context, dict):
                # Add a compact view of context
                context_pairs = ", ".join([f"{k}={v}" for k, v in list(user_context.items())[:10]])
                dynamic_lines.append(f"- User context: {context_pairs}")
            if constraints:
                dynamic_lines.append("- Constraints:")
                for c in constraints[:10]:
                    dynamic_lines.append(f"  * {c}")
            if extra_instructions:
                dynamic_lines.append(f"- Extra instructions: {extra_instructions}")

            examples_block = ""
            if examples:
                formatted = []
                for ex in examples[:5]:
                    u = ex.get("user") or ex.get("input") or ""
                    a = ex.get("assistant") or ex.get("output") or ""
                    formatted.append(f"User: {u}\nAssistant: {a}")
                examples_block = "\n\nFew-shot examples:\n" + "\n\n".join(formatted)

            dynamic_block = ("\n\nDYNAMIC CONTEXT:\n" + "\n".join(dynamic_lines)) if dynamic_lines else ""

            # Create full prompt
            full_prompt = (
                f"{system_prompt}{dynamic_block}{examples_block}\n\n"
                f"User symptoms: {symptoms}\n\n"
                f"Please respond in the LaughRx format:"
            )
            
            # Generate response
            # Allow per-request stop sequences override
            stop_sequences = dynamic_options.get("stop_sequences") if isinstance(dynamic_options, dict) else None
            if not stop_sequences:
                stop_sequences = self.stop_sequences_default or None

            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=self.top_p,
                    top_k=self.top_k,
                    stop_sequences=stop_sequences,
                    max_output_tokens=500,
                )
            )
            
            return {
                "success": True,
                "response": response.text,
                "symptoms": symptoms
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback": "Sorry, I'm having technical difficulties. Please try again!"
            }
    
    def test_multiple_symptoms(self):
        """
        Test with different symptoms
        """
        test_cases = [
            "I have a headache",
            "I can't sleep and feel tired all the time",
            "My back hurts from sitting at my computer",
            "I have a runny nose and feel congested"
        ]
        
        results = []
        
        for symptoms in test_cases:
            print(f"\n{'='*60}")
            print(f"🧪 TESTING: {symptoms}")
            print('='*60)
            
            result = self.generate_response(symptoms)
            
            if result["success"]:
                print("✅ SUCCESS!")
                print(f"\n🤖 LaughRx Response:")
                print(result["response"])
                results.append({"symptoms": symptoms, "success": True})
            else:
                print(f"❌ ERROR: {result['error']}")
                results.append({"symptoms": symptoms, "success": False, "error": result['error']})
        
        return results

def main():
    """
    Main test function
    """
    print("🚀 LaughRx Simple AI Integration Test")
    print("=" * 60)
    print("Testing your AI connection with Google Gemini...")
    print("=" * 60)
    
    try:
        # Initialize AI
        ai = LaughRxAISimple()
        print("✅ AI initialized successfully!")
        print("✅ Connected to Google Gemini Pro!")
        
        # Test single response
        print(f"\n🧪 SINGLE TEST:")
        print("-" * 40)
        
        result = ai.generate_response("I have a headache and feel stressed")
        
        if result["success"]:
            print("✅ AI Response Generated!")
            print(f"\n🤖 LaughRx says:")
            print(result["response"])
        else:
            print(f"❌ Error: {result['error']}")
            return
        
        # Test multiple symptoms
        print(f"\n🧪 MULTIPLE TESTS:")
        print("-" * 40)
        
        results = ai.test_multiple_symptoms()
        
        # Summary
        successful = sum(1 for r in results if r["success"])
        total = len(results)
        
        print(f"\n📊 TEST SUMMARY:")
        print("=" * 60)
        print(f"✅ Successful responses: {successful}/{total}")
        print(f"🎯 Success rate: {(successful/total)*100:.1f}%")
        
        if successful == total:
            print(f"\n🎉 PERFECT! Your LaughRx AI is working!")
            print("✅ All concepts can now be connected to real AI")
            print("✅ Ready to build the complete application")
            
            print(f"\n🔄 NEXT STEPS:")
            print("1. Build FastAPI backend")
            print("2. Create frontend interface") 
            print("3. Deploy to production")
        else:
            print(f"\n⚠️ Some tests failed. Check your API key and internet connection.")
        
    except Exception as e:
        print(f"❌ Setup Error: {e}")
        print(f"\n🔧 TROUBLESHOOTING:")
        print("1. Check GEMINI_API_KEY in .env file")
        print("2. Verify internet connection")
        print("3. Ensure dependencies are installed: pip install google-generativeai python-dotenv")

if __name__ == "__main__":
    main()