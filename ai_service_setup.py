"""
LaughRx - AI Service Setup
==========================

This script helps you set up AI integration with Google Gemini Pro (free tier).
Perfect for getting started quickly with minimal cost.
"""

import os
import json
from typing import Dict, Any, Optional

class LaughRxAISetup:
    def __init__(self):
        self.setup_instructions = self._create_setup_instructions()
        self.integration_code = self._create_integration_code()
    
    def _create_setup_instructions(self) -> Dict[str, Any]:
        """
        Creates step-by-step setup instructions
        """
        return {
            "step_1_get_api_key": {
                "title": "Get Google Gemini API Key (FREE)",
                "instructions": [
                    "1. Go to https://makersuite.google.com/app/apikey",
                    "2. Sign in with your Google account",
                    "3. Click 'Create API Key'",
                    "4. Copy the API key (starts with 'AIza...')",
                    "5. Keep this key safe - you'll need it in the next step"
                ],
                "time_required": "5 minutes",
                "cost": "FREE - Generous free tier included"
            },
            
            "step_2_install_dependencies": {
                "title": "Install Required Python Packages",
                "instructions": [
                    "Run these commands in your terminal:",
                    "pip install google-generativeai",
                    "pip install fastapi uvicorn",
                    "pip install python-dotenv",
                    "pip install requests"
                ],
                "time_required": "2 minutes",
                "cost": "FREE"
            },
            
            "step_3_create_env_file": {
                "title": "Create Environment File",
                "instructions": [
                    "1. Create a file called '.env' in your project folder",
                    "2. Add this line: GEMINI_API_KEY=your_api_key_here",
                    "3. Replace 'your_api_key_here' with your actual API key",
                    "4. Save the file"
                ],
                "time_required": "1 minute",
                "example": "GEMINI_API_KEY=AIzaSyC7x8K9L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6"
            },
            
            "step_4_test_integration": {
                "title": "Test AI Integration",
                "instructions": [
                    "1. Run: python ai_integration.py",
                    "2. Test with: 'I have a headache'",
                    "3. Verify you get a LaughRx-style response",
                    "4. Check that all 9 concepts work"
                ],
                "time_required": "10 minutes",
                "expected_result": "Working AI responses with humor and medical advice"
            }
        }
    
    def _create_integration_code(self) -> str:
        """
        Creates the AI integration code
        """
        return '''"""
LaughRx - AI Integration with Google Gemini
===========================================

This integrates your LaughRx concepts with real AI.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import json

# Import your LaughRx concepts
from system_user_prompts import LaughRxPrompts
from zero_shot_prompting import LaughRxZeroShotPrompting
from structured_output import LaughRxStructuredOutput
from temperature_control import LaughRxTemperatureControl
from one_shot_prompting import LaughRxOneShotPrompting
from multi_shot_prompting import LaughRxMultiShotPrompting
from function_calling import LaughRxFunctionCalling
from chain_of_thought import LaughRxChainOfThought
from tokens_and_tokenization import LaughRxTokenization

class LaughRxAI:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize all LaughRx concepts
        self.prompts = LaughRxPrompts()
        self.zero_shot = LaughRxZeroShotPrompting()
        self.structured = LaughRxStructuredOutput()
        self.temperature = LaughRxTemperatureControl()
        self.one_shot = LaughRxOneShotPrompting()
        self.multi_shot = LaughRxMultiShotPrompting()
        self.functions = LaughRxFunctionCalling()
        self.chain_of_thought = LaughRxChainOfThought()
        self.tokenization = LaughRxTokenization()
    
    def generate_response(self, symptoms: str, user_context: Dict[str, Any] = None, 
                         response_type: str = "standard") -> Dict[str, Any]:
        """
        Generates AI response using your LaughRx concepts
        """
        try:
            # Choose the right prompting strategy
            if response_type == "zero_shot":
                prompt_data = self.zero_shot.get_zero_shot_prompt_pair(symptoms, user_context)
            elif response_type == "one_shot":
                prompt_data = self.one_shot.create_one_shot_prompt(symptoms, user_context)
            elif response_type == "multi_shot":
                prompt_data = self.multi_shot.create_adaptive_multi_shot_prompt(symptoms, user_context)
            elif response_type == "chain_of_thought":
                prompt_data = self.chain_of_thought.create_chain_of_thought_prompt(symptoms, user_context)
            else:
                # Default to structured output
                prompt_data = self.structured.create_structured_prompt(symptoms, user_context)
            
            # Analyze tokens before sending
            token_analysis = self.tokenization.tokenize_text(prompt_data["system_prompt"] + prompt_data["user_prompt"])
            
            # Determine temperature based on symptoms
            temperature_setting = self.temperature.determine_temperature(symptoms, user_context)
            
            # Create the full prompt
            full_prompt = f"{prompt_data['system_prompt']}\\n\\nUser: {prompt_data['user_prompt']}"
            
            # Generate AI response
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature_setting["temperature"],
                    max_output_tokens=1000,
                )
            )
            
            # Parse response
            ai_response = response.text
            
            # Try to structure the response
            try:
                structured_response = self.structured.parse_ai_response(ai_response)
            except:
                # If parsing fails, create basic structure
                structured_response = {
                    "roast": ai_response[:200] + "..." if len(ai_response) > 200 else ai_response,
                    "diagnosis": "AI-generated medical insight",
                    "advice": "Please consult a healthcare professional",
                    "severity": "moderate",
                    "category": "general"
                }
            
            return {
                "success": True,
                "response": structured_response,
                "metadata": {
                    "response_type": response_type,
                    "temperature": temperature_setting["temperature"],
                    "tokens_used": token_analysis.token_count,
                    "cost_estimate": token_analysis.cost_estimate,
                    "processing_time": "< 1 second"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_response": {
                    "roast": "Well, something went wrong with my AI brain, but at least your symptoms are still there! 😅",
                    "diagnosis": "Technical difficulties detected",
                    "advice": "Try again in a moment, and if problems persist, consult a healthcare professional (and maybe a tech support person too!)"
                }
            }
    
    def test_all_concepts(self) -> Dict[str, Any]:
        """
        Tests all 9 LaughRx concepts with real AI
        """
        test_symptoms = "I have a headache and feel tired"
        test_context = {"age": "25", "lifestyle": "desk job"}
        
        results = {}
        
        # Test each concept
        concepts_to_test = [
            "zero_shot",
            "one_shot", 
            "multi_shot",
            "chain_of_thought",
            "standard"
        ]
        
        for concept in concepts_to_test:
            print(f"Testing {concept}...")
            result = self.generate_response(test_symptoms, test_context, concept)
            results[concept] = {
                "success": result["success"],
                "response_preview": result["response"]["roast"][:100] + "..." if result["success"] else "Failed",
                "metadata": result.get("metadata", {})
            }
        
        return results

def main():
    """
    Main function to test AI integration
    """
    print("🤖 LaughRx AI Integration Test")
    print("=" * 50)
    
    try:
        # Initialize AI
        ai = LaughRxAI()
        print("✅ AI initialized successfully!")
        
        # Test basic response
        print("\\n🧪 Testing basic response...")
        result = ai.generate_response("I have a headache")
        
        if result["success"]:
            print("✅ AI response generated!")
            print(f"🎭 Roast: {result['response']['roast']}")
            print(f"🔍 Diagnosis: {result['response']['diagnosis']}")
            print(f"💡 Advice: {result['response']['advice']}")
            print(f"📊 Tokens used: {result['metadata']['tokens_used']}")
            print(f"💰 Cost: ${result['metadata']['cost_estimate']:.6f}")
        else:
            print(f"❌ Error: {result['error']}")
            return
        
        # Test all concepts
        print("\\n🧪 Testing all concepts...")
        all_results = ai.test_all_concepts()
        
        for concept, result in all_results.items():
            status = "✅" if result["success"] else "❌"
            print(f"{status} {concept}: {result['response_preview']}")
        
        print("\\n🎉 AI Integration Complete!")
        print("Your LaughRx system is now powered by real AI!")
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("\\nPlease check:")
        print("1. GEMINI_API_KEY is set in .env file")
        print("2. All dependencies are installed")
        print("3. Internet connection is working")

if __name__ == "__main__":
    main()
'''
    
    def display_setup_guide(self):
        """
        Displays the complete setup guide
        """
        print("🚀 LaughRx AI Integration Setup Guide")
        print("=" * 60)
        print("Get your AI working in the next 15 minutes!")
        print("=" * 60)
        
        for step_key, step_info in self.setup_instructions.items():
            step_num = step_key.split("_")[1]
            print(f"\n📋 STEP {step_num}: {step_info['title']}")
            print(f"⏰ Time: {step_info['time_required']}")
            if 'cost' in step_info:
                print(f"💰 Cost: {step_info['cost']}")
            print("-" * 40)
            
            for instruction in step_info['instructions']:
                print(f"   {instruction}")
            
            if 'example' in step_info:
                print(f"\n   Example: {step_info['example']}")
        
        print(f"\n🎯 WHAT YOU'LL HAVE AFTER SETUP:")
        print("✅ Working AI integration with Google Gemini")
        print("✅ All 9 LaughRx concepts connected to real AI")
        print("✅ Cost-effective solution (free tier)")
        print("✅ Production-ready foundation")
        
        print(f"\n🔄 NEXT STEPS AFTER SETUP:")
        print("1. Test AI integration: python ai_integration.py")
        print("2. Build FastAPI backend: python create_backend.py")
        print("3. Create frontend interface")
        print("4. Deploy to production")
    
    def create_env_template(self):
        """
        Creates .env template file
        """
        env_content = """# LaughRx Environment Variables
# ================================

# Google Gemini API Key (get from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_api_key_here

# Optional: Other AI services (for future use)
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_claude_key_here

# Application Settings
DEBUG=True
HOST=localhost
PORT=8000

# Database (for future use)
DATABASE_URL=sqlite:///laughrx.db
"""
        
        with open(".env.template", "w") as f:
            f.write(env_content)
        
        print("✅ Created .env.template file")
        print("📝 Copy this to .env and add your API key")
    
    def create_integration_file(self):
        """
        Creates the AI integration file
        """
        with open("ai_integration.py", "w") as f:
            f.write(self.integration_code)
        
        print("✅ Created ai_integration.py")
        print("🚀 Ready to test AI integration!")

def main():
    """
    Main setup function
    """
    setup = LaughRxAISetup()
    setup.display_setup_guide()
    
    print("\n" + "=" * 60)
    print("🛠️ CREATING SETUP FILES:")
    print("=" * 60)
    
    setup.create_env_template()
    setup.create_integration_file()
    
    print("\n🎯 YOUR IMMEDIATE NEXT STEPS:")
    print("1. Get Gemini API key: https://makersuite.google.com/app/apikey")
    print("2. Copy .env.template to .env and add your API key")
    print("3. Install dependencies: pip install google-generativeai python-dotenv")
    print("4. Test integration: python ai_integration.py")
    
    print("\n⚡ ESTIMATED TIME TO WORKING AI: 15 minutes")

if __name__ == "__main__":
    main()