"""
LaughRx - One Shot Prompting Implementation
==========================================

One Shot Prompting means providing the AI with ONE example to guide its responses.
This is more reliable than zero-shot but doesn't require multiple examples.

For LaughRx, this helps:
1. Show the AI exactly how to structure roast + diagnosis + advice
2. Demonstrate the right tone and humor level
3. Provide a template for consistent responses
4. Reduce variability while maintaining creativity
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ExampleType(Enum):
    """Types of examples for different contexts"""
    BASIC_SYMPTOM = "basic_symptom"
    LIFESTYLE_ISSUE = "lifestyle_issue"
    WELLNESS_QUESTION = "wellness_question"
    MINOR_INJURY = "minor_injury"

@dataclass
class OneShotExample:
    """Structure for one-shot examples"""
    user_input: str
    ai_response: str
    context: str
    explanation: str

class LaughRxOneShotPrompting:
    def __init__(self):
        self.examples = self._create_one_shot_examples()
        self.base_system_prompt = self._create_base_system_prompt()
    
    def _create_base_system_prompt(self) -> str:
        """
        Creates the base system prompt that works with one-shot examples
        """
        return """You are LaughRx, the AI Roast Doctor. You provide humorous yet helpful medical advice.

Your responses must ALWAYS follow this structure:
1. ROAST: A witty, playful observation about their lifestyle or symptoms (2-3 sentences)
2. DIAGNOSIS: A possible medical explanation in simple terms (1-2 sentences)
3. ADVICE: Practical, actionable health advice (2-4 sentences)

PERSONALITY GUIDELINES:
- Be funny but never mean-spirited
- Connect symptoms to common lifestyle choices
- Use casual, friendly language
- Show empathy through humor
- Always end with medical disclaimer

MEDICAL RESPONSIBILITY:
- Never diagnose serious conditions definitively
- Always recommend professional consultation for concerning symptoms
- Focus on general wellness and lifestyle advice
- Avoid specific medication recommendations"""

    def _create_one_shot_examples(self) -> Dict[ExampleType, OneShotExample]:
        """
        Creates one-shot examples for different types of interactions
        """
        return {
            ExampleType.BASIC_SYMPTOM: OneShotExample(
                user_input="I have a headache and feel tired",
                ai_response="""🎭 ROAST: Let me guess - you've been living on coffee and screen time while treating water like it's optional? Your brain is probably sending you a strongly worded complaint about your lifestyle choices! ☕💻

🔍 DIAGNOSIS: This sounds like a classic combination of dehydration and digital eye strain, possibly with some caffeine withdrawal thrown in for good measure.

💡 ADVICE: Time for some revolutionary self-care: drink actual water (shocking, I know!), take breaks from screens every 20 minutes, and maybe get some fresh air. Your head will stop plotting revenge against you. If headaches persist or worsen, please consult a healthcare professional - I'm just here for the roasts and basic wisdom!""",
                context="Common symptom with lifestyle factors",
                explanation="Shows how to connect symptoms to lifestyle with humor while providing practical advice"
            ),
            
            ExampleType.LIFESTYLE_ISSUE: OneShotExample(
                user_input="I sit at a desk all day and my back hurts",
                ai_response="""🎭 ROAST: Ah, the classic "human pretzel" transformation! You've successfully evolved from Homo sapiens to Homo deskicus - congratulations on becoming one with your chair! 🪑🥨

🔍 DIAGNOSIS: You're experiencing postural strain and muscle tension from prolonged sitting, which is basically your spine's way of staging a rebellion against modern office life.

💡 ADVICE: Time to break up this toxic relationship with your chair! Stand and stretch every 30 minutes, do some desk exercises, and maybe invest in ergonomic furniture. Your spine will stop sending you hate mail. For persistent back pain, consider seeing a physical therapist or healthcare provider.""",
                context="Work-related physical issue",
                explanation="Demonstrates how to roast lifestyle choices while providing ergonomic advice"
            ),
            
            ExampleType.WELLNESS_QUESTION: OneShotExample(
                user_input="I want to start eating healthier but don't know where to begin",
                ai_response="""🎭 ROAST: Let me paint a picture: your current diet consists of whatever's fastest, your vegetables come in chip form, and you consider ketchup a serving of tomatoes! Time to break up with processed foods - they're not good for you! 🍟💔

🔍 DIAGNOSIS: You're suffering from "convenience food syndrome" - a very common condition in the modern world where real food seems like a foreign concept.

💡 ADVICE: Start small and simple: add one actual vegetable to each meal, drink more water, and maybe visit the produce section (it's that colorful area in the grocery store). Don't try to change everything at once - your taste buds need time to adjust to real flavors! For personalized nutrition advice, consider consulting a registered dietitian.""",
                context="Nutrition and wellness guidance",
                explanation="Shows encouraging tone for positive lifestyle changes"
            ),
            
            ExampleType.MINOR_INJURY: OneShotExample(
                user_input="I twisted my ankle while running",
                ai_response="""🎭 ROAST: Ah, the classic "I'm basically an athlete" moment meets reality! Your ankle just gave you a gentle reminder that enthusiasm doesn't always equal coordination. Welcome to the "oops" club! 🏃‍♂️💥

🔍 DIAGNOSIS: Sounds like a minor ankle sprain - your ligaments got a bit overstretched when your foot decided to go on an unplanned adventure.

💡 ADVICE: Time for the RICE protocol: Rest, Ice, Compression, Elevation. Take it easy for a few days, ice for 15-20 minutes at a time, and keep that ankle elevated when possible. If pain is severe, you can't bear weight, or it doesn't improve in a few days, definitely see a healthcare provider to rule out fractures.""",
                context="Minor sports injury",
                explanation="Balances humor with practical first aid advice"
            )
        }
    
    def create_one_shot_prompt(self, symptoms: str, example_type: ExampleType = ExampleType.BASIC_SYMPTOM, user_context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Creates a one-shot prompt with example and user input
        """
        example = self.examples[example_type]
        
        # Build the complete prompt with example
        system_prompt = f"""{self.base_system_prompt}

Here's an example of how you should respond:

USER: {example.user_input}

LAUGHRX: {example.ai_response}

Now respond to the new user input in the same style and format."""
        
        # Create user prompt
        user_prompt = f"USER: {symptoms}"
        if user_context:
            context_parts = [f"{k}: {v}" for k, v in user_context.items()]
            user_prompt += f"\nContext: {', '.join(context_parts)}"
        
        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "example_used": example_type.value,
            "example_explanation": example.explanation
        }
    
    def determine_best_example(self, symptoms: str) -> ExampleType:
        """
        Determines which example would be most appropriate for the given symptoms
        """
        symptoms_lower = symptoms.lower()
        
        # Check for wellness/lifestyle questions
        wellness_keywords = ['eat', 'diet', 'nutrition', 'exercise', 'fitness', 'healthy', 'weight', 'lifestyle']
        if any(keyword in symptoms_lower for keyword in wellness_keywords):
            return ExampleType.WELLNESS_QUESTION
        
        # Check for work-related issues
        work_keywords = ['desk', 'office', 'computer', 'sitting', 'back', 'neck', 'posture']
        if any(keyword in symptoms_lower for keyword in work_keywords):
            return ExampleType.LIFESTYLE_ISSUE
        
        # Check for injuries
        injury_keywords = ['twisted', 'sprained', 'hurt', 'injured', 'fell', 'running', 'sports']
        if any(keyword in symptoms_lower for keyword in injury_keywords):
            return ExampleType.MINOR_INJURY
        
        # Default to basic symptom
        return ExampleType.BASIC_SYMPTOM
    
    def create_adaptive_one_shot_prompt(self, symptoms: str, user_context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Creates a one-shot prompt with automatically selected best example
        """
        best_example = self.determine_best_example(symptoms)
        return self.create_one_shot_prompt(symptoms, best_example, user_context)
    
    def compare_zero_shot_vs_one_shot(self, symptoms: str) -> Dict[str, Any]:
        """
        Compares zero-shot vs one-shot approaches for the same symptom
        """
        # Zero-shot prompt (no example)
        zero_shot_prompt = f"""{self.base_system_prompt}

USER: {symptoms}"""
        
        # One-shot prompt (with example)
        one_shot_data = self.create_adaptive_one_shot_prompt(symptoms)
        
        return {
            "symptom": symptoms,
            "zero_shot": {
                "prompt": zero_shot_prompt,
                "characteristics": ["No guidance", "More unpredictable", "Relies on system prompt only"],
                "pros": ["Flexible", "No bias from examples"],
                "cons": ["Less consistent", "May miss format requirements"]
            },
            "one_shot": {
                "prompt": one_shot_data["system_prompt"],
                "example_used": one_shot_data["example_used"],
                "characteristics": ["Clear example provided", "More predictable format", "Guided by template"],
                "pros": ["Consistent structure", "Better format adherence", "Clearer expectations"],
                "cons": ["May be influenced by example", "Less creative variation"]
            }
        }
    
    def demonstrate_one_shot_prompting(self):
        """
        Demonstrates one-shot prompting with various examples
        """
        print("🎯 LaughRx - One Shot Prompting Demo")
        print("=" * 60)
        print("One Shot = Provide ONE example to guide AI responses!")
        print("=" * 60)
        
        # Show all available examples
        print("\n📚 AVAILABLE ONE-SHOT EXAMPLES:")
        print("-" * 50)
        
        for example_type, example in self.examples.items():
            print(f"\n🎭 {example_type.value.upper().replace('_', ' ')}:")
            print(f"   Context: {example.context}")
            print(f"   User Input: \"{example.user_input}\"")
            print(f"   Purpose: {example.explanation}")
        
        # Demonstrate adaptive example selection
        print(f"\n🤖 ADAPTIVE EXAMPLE SELECTION:")
        print("-" * 50)
        
        test_cases = [
            "I have a headache",
            "My back hurts from sitting all day",
            "I want to start eating better",
            "I sprained my wrist playing tennis"
        ]
        
        for symptom in test_cases:
            best_example = self.determine_best_example(symptom)
            print(f"\n💬 Symptom: \"{symptom}\"")
            print(f"   → Best Example: {best_example.value}")
            print(f"   → Reasoning: {self.examples[best_example].explanation}")
        
        # Compare zero-shot vs one-shot
        print(f"\n⚖️ ZERO-SHOT VS ONE-SHOT COMPARISON:")
        print("-" * 50)
        
        comparison = self.compare_zero_shot_vs_one_shot("I can't sleep at night")
        print(f"\nSymptom: \"{comparison['symptom']}\"")
        
        print(f"\n🔸 ZERO-SHOT APPROACH:")
        for char in comparison['zero_shot']['characteristics']:
            print(f"   • {char}")
        
        print(f"\n🔹 ONE-SHOT APPROACH:")
        print(f"   Example Used: {comparison['one_shot']['example_used']}")
        for char in comparison['one_shot']['characteristics']:
            print(f"   • {char}")

def main():
    """
    Main function to demonstrate one-shot prompting
    """
    one_shot_system = LaughRxOneShotPrompting()
    one_shot_system.demonstrate_one_shot_prompting()
    
    print("\n" + "=" * 60)
    print("🎯 ONE SHOT PROMPTING - KEY BENEFITS:")
    print("=" * 60)
    print("✅ Consistent Format: Example shows exact structure to follow")
    print("✅ Better Quality: AI understands tone and style from example")
    print("✅ Reduced Variability: More predictable than zero-shot")
    print("✅ Adaptive Examples: Different examples for different contexts")
    print("✅ Template Learning: AI learns pattern from single example")
    
    print("\n🔬 WHEN TO USE ONE-SHOT VS ZERO-SHOT:")
    print("• One-Shot: When you need consistent format and tone")
    print("• Zero-Shot: When you want maximum flexibility and creativity")
    print("• One-Shot: For complex response structures")
    print("• Zero-Shot: For simple, straightforward responses")
    
    print("\n🔄 NEXT CONCEPTS TO IMPLEMENT:")
    print("- Multi Shot Prompting (multiple examples)")
    print("- Function Calling (dynamic advice)")
    print("- Chain of Thought (step-by-step reasoning)")

if __name__ == "__main__":
    main()