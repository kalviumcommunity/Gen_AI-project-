"""
LaughRx - System and User Prompt Implementation
==============================================

This demonstrates how System and User prompts work together to create
the AI doctor's personality and handle user interactions.

System Prompt: Defines the AI's role, personality, and behavior rules
User Prompt: Contains the actual user input/symptoms
"""

import os
from typing import Dict, Any

class LaughRxPrompts:
    def __init__(self):
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """
        Creates the system prompt that defines LaughRx's personality
        """
        return """You are LaughRx, a humorous AI doctor with a unique personality:

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
- Show empathy while being funny

MEDICAL RESPONSIBILITY:
- Never diagnose serious conditions definitively
- Always suggest consulting healthcare professionals
- Provide general wellness advice only
- Avoid giving specific medication recommendations

Remember: You're like a funny friend who happens to know about health, not a replacement for real medical care."""

    def create_user_prompt(self, symptoms: str, user_context: Dict[str, Any] = None) -> str:
        """
        Creates the user prompt with symptoms and optional context
        
        Args:
            symptoms (str): User's reported symptoms
            user_context (dict): Optional context like age, lifestyle, etc.
        """
        base_prompt = f"User's symptoms: {symptoms}"
        
        if user_context:
            context_info = []
            if user_context.get('age'):
                context_info.append(f"Age: {user_context['age']}")
            if user_context.get('lifestyle'):
                context_info.append(f"Lifestyle: {user_context['lifestyle']}")
            if user_context.get('previous_issues'):
                context_info.append(f"Previous issues: {user_context['previous_issues']}")
            
            if context_info:
                base_prompt += f"\nAdditional context: {', '.join(context_info)}"
        
        return base_prompt
    
    def get_complete_prompt(self, symptoms: str, user_context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Returns both system and user prompts ready for AI model
        """
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": self.create_user_prompt(symptoms, user_context)
        }
    
    def demonstrate_prompts(self):
        """
        Demonstrates different prompt combinations
        """
        print("🤖 LaughRx - System and User Prompt Demo")
        print("=" * 50)
        
        # Example 1: Basic symptoms
        print("\n📝 EXAMPLE 1: Basic Symptoms")
        print("-" * 30)
        prompts1 = self.get_complete_prompt("I have a headache")
        print("SYSTEM PROMPT:")
        print(prompts1["system_prompt"][:200] + "...")
        print(f"\nUSER PROMPT:")
        print(prompts1["user_prompt"])
        
        # Example 2: With context
        print("\n📝 EXAMPLE 2: With User Context")
        print("-" * 30)
        context = {
            "age": "25",
            "lifestyle": "works long hours on computer",
            "previous_issues": "occasional migraines"
        }
        prompts2 = self.get_complete_prompt("I have a severe headache and eye strain", context)
        print("SYSTEM PROMPT: [Same as above]")
        print(f"\nUSER PROMPT:")
        print(prompts2["user_prompt"])
        
        # Example 3: Different symptoms
        print("\n📝 EXAMPLE 3: Different Symptoms")
        print("-" * 30)
        prompts3 = self.get_complete_prompt("I can't sleep and I'm always tired")
        print("SYSTEM PROMPT: [Same as above]")
        print(f"\nUSER PROMPT:")
        print(prompts3["user_prompt"])

def main():
    """
    Main function to demonstrate the prompt system
    """
    prompt_system = LaughRxPrompts()
    prompt_system.demonstrate_prompts()
    
    print("\n" + "=" * 50)
    print("🎯 KEY CONCEPTS DEMONSTRATED:")
    print("=" * 50)
    print("✅ System Prompt: Defines AI personality and behavior rules")
    print("✅ User Prompt: Contains user input and context")
    print("✅ Prompt Engineering: Structured instructions for consistent responses")
    print("✅ Context Integration: Adding user background for better responses")
    print("✅ Responsible AI: Built-in safety and medical disclaimers")
    
    print("\n🔄 NEXT CONCEPTS TO IMPLEMENT:")
    print("- Zero Shot Prompting (responses without examples)")
    print("- Structured Output (JSON format)")
    print("- Temperature control (response randomness)")

if __name__ == "__main__":
    main()