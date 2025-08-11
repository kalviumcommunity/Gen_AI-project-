"""
LaughRx - Zero Shot Prompting Implementation
==========================================

Zero Shot Prompting means getting the AI to perform a task without providing
any examples - just clear instructions in the system prompt.

This is perfect for LaughRx because we want the AI to:
1. Generate unique roasts for any symptom
2. Provide medical advice without seeing examples first
3. Maintain consistent personality across all interactions
"""

import json
from typing import Dict, Any, List

class LaughRxZeroShotPrompting:
    def __init__(self):
        self.system_prompt = self._create_zero_shot_system_prompt()
    
    def _create_zero_shot_system_prompt(self) -> str:
        """
        Creates a comprehensive system prompt that enables zero-shot responses
        The key is being very specific about what we want without showing examples
        """
        return """You are LaughRx, the AI Roast Doctor. Your job is to respond to ANY medical symptom or health concern with humor and helpful advice.

ZERO-SHOT RESPONSE RULES:
For ANY symptom the user mentions, you must ALWAYS follow this exact structure:

1. ROAST SECTION (2-3 sentences):
   - Make a playful, light-hearted joke about their lifestyle or the symptom
   - Be witty but never mean or offensive
   - Connect the symptom to common lifestyle choices (screen time, diet, sleep, etc.)

2. DIAGNOSIS SECTION (1-2 sentences):
   - Provide a possible explanation for their symptoms
   - Use medical knowledge but keep it accessible
   - Never make definitive diagnoses for serious conditions

3. ADVICE SECTION (2-4 sentences):
   - Give practical, actionable health advice
   - Include both immediate relief and prevention tips
   - Always end with "consult a healthcare professional if symptoms persist"

PERSONALITY TRAITS TO MAINTAIN:
- Witty and observational (like a comedian who studied medicine)
- Caring but sarcastic
- Knowledgeable but not pretentious
- Always responsible about serious health concerns

TOPICS YOU CAN HANDLE (zero-shot):
- Common symptoms: headaches, fatigue, stomach issues, sleep problems
- Lifestyle issues: stress, poor posture, eye strain
- Minor injuries: cuts, bruises, muscle soreness
- Wellness questions: diet, exercise, mental health basics

SAFETY RULES:
- Never diagnose serious conditions (cancer, heart disease, etc.)
- Always recommend professional help for severe symptoms
- Don't prescribe specific medications
- If unsure, err on the side of caution

Remember: You're seeing each symptom for the "first time" - no examples needed, just apply your personality and medical knowledge consistently."""

    def create_zero_shot_prompt(self, symptoms: str, user_context: Dict[str, Any] = None) -> str:
        """
        Creates a user prompt that works with zero-shot prompting
        No examples provided - the AI must figure it out from system instructions
        """
        prompt = f"Please help me with these symptoms: {symptoms}"
        
        if user_context:
            context_parts = []
            for key, value in user_context.items():
                context_parts.append(f"{key}: {value}")
            
            if context_parts:
                prompt += f"\n\nAdditional information about me: {', '.join(context_parts)}"
        
        prompt += "\n\nPlease respond in your typical LaughRx style with a roast, diagnosis, and advice."
        
        return prompt
    
    def get_zero_shot_prompt_pair(self, symptoms: str, user_context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Returns the complete prompt pair for zero-shot prompting
        """
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": self.create_zero_shot_prompt(symptoms, user_context)
        }
    
    def simulate_zero_shot_responses(self) -> List[Dict[str, Any]]:
        """
        Simulates what zero-shot responses would look like for different symptoms
        This shows how the same system prompt handles various inputs without examples
        """
        test_cases = [
            {
                "symptoms": "I have a headache",
                "context": None,
                "expected_pattern": "Screen time joke → tension headache → hydration advice"
            },
            {
                "symptoms": "I can't sleep at night",
                "context": {"age": "28", "job": "software developer"},
                "expected_pattern": "Caffeine/screen joke → sleep hygiene → bedtime routine advice"
            },
            {
                "symptoms": "My back hurts from sitting all day",
                "context": {"lifestyle": "desk job"},
                "expected_pattern": "Posture joke → muscle tension → ergonomic advice"
            },
            {
                "symptoms": "I feel tired all the time",
                "context": None,
                "expected_pattern": "Lifestyle joke → possible causes → energy improvement tips"
            },
            {
                "symptoms": "I have stomach pain after eating",
                "context": {"diet": "fast food lover"},
                "expected_pattern": "Diet joke → digestive issues → eating habit advice"
            }
        ]
        
        return test_cases
    
    def demonstrate_zero_shot_prompting(self):
        """
        Demonstrates zero-shot prompting with various examples
        """
        print("🎯 LaughRx - Zero Shot Prompting Demo")
        print("=" * 60)
        print("Zero Shot = AI responds to ANY symptom without seeing examples first!")
        print("=" * 60)
        
        test_cases = self.simulate_zero_shot_responses()
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n🧪 TEST CASE {i}: {case['symptoms']}")
            print("-" * 40)
            
            # Show the prompt pair
            prompts = self.get_zero_shot_prompt_pair(case['symptoms'], case['context'])
            
            print("📝 SYSTEM PROMPT (First 200 chars):")
            print(f"'{prompts['system_prompt'][:200]}...'")
            
            print(f"\n💬 USER PROMPT:")
            print(f"'{prompts['user_prompt']}'")
            
            print(f"\n🎭 EXPECTED RESPONSE PATTERN:")
            print(f"'{case['expected_pattern']}'")
            
            print(f"\n🤖 SIMULATED LAUGHRX RESPONSE:")
            print(self._simulate_response(case['symptoms'], case['context']))
    
    def _simulate_response(self, symptoms: str, context: Dict[str, Any] = None) -> str:
        """
        Simulates what LaughRx would respond (since we don't have actual AI here)
        This shows the zero-shot prompting concept in action
        """
        # This is a simulation - in real implementation, this would be the AI's response
        responses = {
            "I have a headache": "Oh, let me guess - you've been best friends with your screen today and water is just a distant memory? 🖥️💧 This sounds like a classic tension headache, probably from dehydration or eye strain. Here's your prescription: drink some H2O (revolutionary!), take a screen break, and maybe step outside. If this keeps happening, consult a real doctor - I'm just here for the roasts and basic wisdom! 😄",
            
            "I can't sleep at night": "Ah, the classic 'I'll just scroll for 5 more minutes at midnight' syndrome! 📱🌙 As a software developer, I bet your brain is still debugging code when you hit the pillow. Try the 3-2-1 rule: no screens 3 hours before bed, no food 2 hours before, and 1 hour of relaxing activities. Your sleep schedule will thank you! If insomnia persists, see a healthcare professional. 💤",
            
            "My back hurts from sitting all day": "Welcome to the 'human pretzel' club! Your spine is probably shaped like a question mark from all that desk sitting. 🪑😵 This is classic postural strain from prolonged sitting. Time for some movement therapy: stand every 30 minutes, do some stretches, and maybe invest in ergonomic furniture. Your back will stop plotting revenge against you! If pain continues, consult a healthcare provider. 🏃‍♂️",
            
            "I feel tired all the time": "Ah, the eternal zombie state! Let me guess - your sleep schedule is more like a suggestion and coffee is your main food group? ☕🧟 Chronic fatigue can have many causes: poor sleep, stress, diet, or underlying conditions. Start with sleep hygiene, balanced meals, and regular exercise. If exhaustion persists, definitely see a doctor to rule out medical causes! 😴",
            
            "I have stomach pain after eating": "Fast food lover, eh? Your stomach is probably staging a protest against your culinary choices! 🍔😤 This sounds like digestive upset, possibly from rich, processed foods or eating too quickly. Try smaller meals, chew slowly, and maybe befriend some vegetables. If stomach pain continues or worsens, consult a healthcare professional - your gut health matters! 🥗"
        }
        
        return responses.get(symptoms, "I'd roast you about this symptom, but I need more details to craft the perfect comedic diagnosis! 😄")

def main():
    """
    Main function to demonstrate zero-shot prompting
    """
    zero_shot_system = LaughRxZeroShotPrompting()
    zero_shot_system.demonstrate_zero_shot_prompting()
    
    print("\n" + "=" * 60)
    print("🎯 ZERO SHOT PROMPTING - KEY CONCEPTS:")
    print("=" * 60)
    print("✅ No Examples Needed: AI responds to ANY symptom without prior examples")
    print("✅ Consistent Personality: Same humorous doctor tone for all responses")
    print("✅ Flexible Input Handling: Works with any symptom or health concern")
    print("✅ Reliable Structure: Always follows roast → diagnosis → advice pattern")
    print("✅ Scalable: Can handle unlimited symptom variations")
    
    print("\n🔬 WHY ZERO SHOT IS PERFECT FOR LAUGHRX:")
    print("- Users can ask about ANY health concern")
    print("- No need to pre-program responses for every symptom")
    print("- AI generates unique, contextual roasts every time")
    print("- Maintains medical responsibility across all responses")
    
    print("\n🔄 NEXT CONCEPTS TO IMPLEMENT:")
    print("- Structured Output (JSON format for frontend)")
    print("- Temperature Control (response creativity)")
    print("- One Shot Prompting (providing examples)")

if __name__ == "__main__":
    main()