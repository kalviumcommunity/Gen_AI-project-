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
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        print(f"🎯 Generation top_p set to: {self.top_p}, top_k set to: {self.top_k}")
        
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
    
    def generate_response(self, symptoms: str) -> dict:
        """
        Generate AI response for symptoms
        """
        try:
            # Create full prompt
            full_prompt = f"{self.system_prompt}\n\nUser symptoms: {symptoms}\n\nPlease respond in the LaughRx format:"
            
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=self.top_p,
                    top_k=self.top_k,
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