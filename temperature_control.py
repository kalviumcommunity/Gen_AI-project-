"""
LaughRx - Temperature Control Implementation
==========================================

Temperature controls the randomness/creativity of AI responses:
- Low Temperature (0.1-0.3): More predictable, consistent, conservative
- Medium Temperature (0.4-0.7): Balanced creativity and reliability  
- High Temperature (0.8-1.0): More creative, unpredictable, varied

For LaughRx, this is crucial because:
1. Medical advice needs to be consistent (low temperature)
2. Roasts can be more creative (higher temperature)
3. Emergency situations need predictable responses (very low temperature)
"""

from typing import Dict, Any, List
from enum import Enum
from dataclasses import dataclass

class TemperatureLevel(Enum):
    """Temperature levels for different response types"""
    CONSERVATIVE = 0.2    # Medical advice, emergency responses
    BALANCED = 0.5        # General health advice
    CREATIVE = 0.8        # Roasts and humor
    EXPERIMENTAL = 1.0    # Maximum creativity (use carefully)

class ResponseContext(Enum):
    """Different contexts that require different temperature settings"""
    EMERGENCY = "emergency"
    SERIOUS_MEDICAL = "serious_medical"
    GENERAL_HEALTH = "general_health"
    WELLNESS_TIP = "wellness_tip"
    HUMOR_ROAST = "humor_roast"

@dataclass
class TemperatureConfig:
    """Configuration for temperature settings based on context"""
    context: ResponseContext
    temperature: float
    description: str
    use_case: str

class LaughRxTemperatureControl:
    def __init__(self):
        self.temperature_configs = self._create_temperature_configs()
        self.system_prompts = self._create_context_specific_prompts()
    
    def _create_temperature_configs(self) -> Dict[ResponseContext, TemperatureConfig]:
        """
        Creates temperature configurations for different contexts
        """
        return {
            ResponseContext.EMERGENCY: TemperatureConfig(
                context=ResponseContext.EMERGENCY,
                temperature=0.1,
                description="Very low temperature for consistent, reliable emergency responses",
                use_case="Chest pain, severe symptoms, immediate medical attention needed"
            ),
            ResponseContext.SERIOUS_MEDICAL: TemperatureConfig(
                context=ResponseContext.SERIOUS_MEDICAL,
                temperature=0.3,
                description="Low temperature for consistent medical advice",
                use_case="Chronic conditions, medication questions, concerning symptoms"
            ),
            ResponseContext.GENERAL_HEALTH: TemperatureConfig(
                context=ResponseContext.GENERAL_HEALTH,
                temperature=0.5,
                description="Balanced temperature for reliable yet engaging responses",
                use_case="Common symptoms like headaches, fatigue, minor issues"
            ),
            ResponseContext.WELLNESS_TIP: TemperatureConfig(
                context=ResponseContext.WELLNESS_TIP,
                temperature=0.6,
                description="Moderate temperature for engaging wellness advice",
                use_case="Exercise tips, nutrition advice, lifestyle improvements"
            ),
            ResponseContext.HUMOR_ROAST: TemperatureConfig(
                context=ResponseContext.HUMOR_ROAST,
                temperature=0.8,
                description="High temperature for creative, varied roasts",
                use_case="Humorous observations about lifestyle choices"
            )
        }
    
    def _create_context_specific_prompts(self) -> Dict[ResponseContext, str]:
        """
        Creates system prompts optimized for different temperature settings
        """
        return {
            ResponseContext.EMERGENCY: """You are LaughRx in EMERGENCY MODE. 

CRITICAL: Skip humor entirely. Be direct, clear, and consistent.

For emergency symptoms (chest pain, severe bleeding, difficulty breathing, etc.):
1. Immediately recommend emergency medical care
2. Provide clear, actionable steps
3. Use consistent, reliable language
4. No jokes or roasts - this is serious

Always respond with the same level of urgency and clarity.""",

            ResponseContext.SERIOUS_MEDICAL: """You are LaughRx in SERIOUS MEDICAL MODE.

Use minimal humor and focus on reliable medical guidance.

For concerning symptoms:
1. Light, respectful tone (minimal roasting)
2. Consistent medical explanations
3. Clear, actionable advice
4. Strong emphasis on professional consultation

Maintain professionalism while keeping some personality.""",

            ResponseContext.GENERAL_HEALTH: """You are LaughRx in BALANCED MODE.

Perfect balance of humor and medical responsibility.

For common symptoms:
1. Moderate roasting about lifestyle choices
2. Reliable medical explanations
3. Practical advice with personality
4. Consistent structure: roast → diagnosis → advice

This is your standard operating mode.""",

            ResponseContext.WELLNESS_TIP: """You are LaughRx in WELLNESS MODE.

Be encouraging and moderately humorous about healthy lifestyle choices.

For wellness questions:
1. Gentle, motivational roasting
2. Positive, encouraging explanations
3. Actionable wellness advice
4. Focus on building healthy habits

Be supportive while maintaining your wit.""",

            ResponseContext.HUMOR_ROAST: """You are LaughRx in CREATIVE ROAST MODE.

Maximum creativity for humorous observations (while staying appropriate).

For lifestyle roasting:
1. Creative, varied jokes about habits
2. Witty observations about modern life
3. Playful but never mean-spirited
4. Highly creative language and metaphors

Let your comedic creativity shine while staying helpful!"""
        }
    
    def determine_context(self, symptoms: str, user_context: Dict[str, Any] = None) -> ResponseContext:
        """
        Determines the appropriate context based on symptoms
        """
        symptoms_lower = symptoms.lower()
        
        # Emergency keywords
        emergency_keywords = [
            'chest pain', 'heart attack', 'can\'t breathe', 'shortness of breath',
            'severe bleeding', 'unconscious', 'stroke', 'seizure', 'overdose',
            'severe allergic reaction', 'choking'
        ]
        
        # Serious medical keywords
        serious_keywords = [
            'chronic pain', 'depression', 'anxiety', 'medication', 'prescription',
            'blood pressure', 'diabetes', 'cancer', 'tumor', 'infection'
        ]
        
        # Wellness keywords
        wellness_keywords = [
            'exercise', 'diet', 'nutrition', 'weight loss', 'fitness',
            'healthy habits', 'lifestyle', 'prevention', 'wellness'
        ]
        
        # Check for emergency
        if any(keyword in symptoms_lower for keyword in emergency_keywords):
            return ResponseContext.EMERGENCY
        
        # Check for serious medical
        if any(keyword in symptoms_lower for keyword in serious_keywords):
            return ResponseContext.SERIOUS_MEDICAL
        
        # Check for wellness
        if any(keyword in symptoms_lower for keyword in wellness_keywords):
            return ResponseContext.WELLNESS_TIP
        
        # Default to general health
        return ResponseContext.GENERAL_HEALTH
    
    def get_temperature_config(self, symptoms: str, user_context: Dict[str, Any] = None) -> TemperatureConfig:
        """
        Gets the appropriate temperature configuration for given symptoms
        """
        context = self.determine_context(symptoms, user_context)
        return self.temperature_configs[context]
    
    def create_temperature_aware_prompt(self, symptoms: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Creates a prompt with appropriate temperature setting
        """
        config = self.get_temperature_config(symptoms, user_context)
        system_prompt = self.system_prompts[config.context]
        
        user_prompt = f"Symptoms: {symptoms}"
        if user_context:
            context_parts = [f"{k}: {v}" for k, v in user_context.items()]
            user_prompt += f"\nContext: {', '.join(context_parts)}"
        
        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "temperature": config.temperature,
            "context": config.context.value,
            "description": config.description,
            "use_case": config.use_case
        }
    
    def simulate_temperature_effects(self) -> List[Dict[str, Any]]:
        """
        Simulates how different temperatures affect responses
        """
        test_symptom = "I have a headache"
        
        return [
            {
                "temperature": 0.1,
                "description": "Very Conservative",
                "response": "You have a headache. This is commonly caused by dehydration or tension. Drink water and rest. Consult a doctor if it persists.",
                "characteristics": ["Predictable", "Consistent", "Medical focus", "No creativity"]
            },
            {
                "temperature": 0.3,
                "description": "Conservative",
                "response": "You're experiencing a headache, likely from dehydration or stress. Try drinking water and taking a break from screens. See a healthcare provider if symptoms continue.",
                "characteristics": ["Reliable", "Slightly varied", "Professional tone", "Minimal humor"]
            },
            {
                "temperature": 0.5,
                "description": "Balanced",
                "response": "Let me guess - you've been staring at screens and forgot water exists? This sounds like a tension headache. Drink some H2O, take screen breaks, and rest. If it persists, consult a doctor.",
                "characteristics": ["Good balance", "Some humor", "Engaging", "Reliable advice"]
            },
            {
                "temperature": 0.7,
                "description": "Creative",
                "response": "Ah, the classic 'screen zombie' syndrome strikes again! Your brain is probably staging a dehydration protest. Time for some revolutionary H2O therapy and maybe stepping away from the digital overlords!",
                "characteristics": ["More creative", "Varied language", "Engaging humor", "Personality-driven"]
            },
            {
                "temperature": 0.9,
                "description": "Highly Creative",
                "response": "Behold! The mighty screen-staring warrior has fallen victim to the ancient curse of the dehydrated cranium! Your neural pathways are crying out for the mystical elixir known as... water! 🧙‍♂️💧",
                "characteristics": ["Very creative", "Unpredictable", "Highly varied", "Risk of inconsistency"]
            }
        ]
    
    def demonstrate_temperature_control(self):
        """
        Demonstrates temperature control with various examples
        """
        print("🌡️ LaughRx - Temperature Control Demo")
        print("=" * 60)
        print("Temperature = Controls AI creativity vs. consistency!")
        print("=" * 60)
        
        # Show different contexts and their temperatures
        print("\n📊 CONTEXT-BASED TEMPERATURE SETTINGS:")
        print("-" * 50)
        
        for context, config in self.temperature_configs.items():
            print(f"\n🎯 {context.value.upper().replace('_', ' ')}")
            print(f"   Temperature: {config.temperature}")
            print(f"   Description: {config.description}")
            print(f"   Use Case: {config.use_case}")
        
        # Show temperature effects
        print(f"\n🧪 TEMPERATURE EFFECTS ON SAME SYMPTOM:")
        print("-" * 50)
        
        effects = self.simulate_temperature_effects()
        for effect in effects:
            print(f"\n🌡️ Temperature {effect['temperature']} ({effect['description']}):")
            print(f"   Response: \"{effect['response']}\"")
            print(f"   Characteristics: {', '.join(effect['characteristics'])}")
        
        # Show real examples
        print(f"\n🎭 REAL CONTEXT EXAMPLES:")
        print("-" * 50)
        
        test_cases = [
            ("I have chest pain and can't breathe", None),
            ("I've been feeling depressed lately", {"age": "30"}),
            ("I have a headache from work", None),
            ("I want to start exercising", {"lifestyle": "sedentary"}),
        ]
        
        for symptoms, context in test_cases:
            print(f"\n💬 Symptom: \"{symptoms}\"")
            config = self.get_temperature_config(symptoms, context)
            print(f"   → Context: {config.context.value}")
            print(f"   → Temperature: {config.temperature}")
            print(f"   → Reasoning: {config.description}")

def main():
    """
    Main function to demonstrate temperature control
    """
    temp_system = LaughRxTemperatureControl()
    temp_system.demonstrate_temperature_control()
    
    print("\n" + "=" * 60)
    print("🎯 TEMPERATURE CONTROL - KEY BENEFITS:")
    print("=" * 60)
    print("✅ Context-Aware: Different temperatures for different situations")
    print("✅ Medical Safety: Low temperature for serious/emergency responses")
    print("✅ Engaging Humor: Higher temperature for creative roasts")
    print("✅ Consistent Quality: Balanced approach prevents extremes")
    print("✅ User Experience: Appropriate tone for each interaction")
    
    print("\n🔬 WHY TEMPERATURE MATTERS FOR LAUGHRX:")
    print("- Emergency responses must be consistent and reliable")
    print("- Roasts can be creative and varied for entertainment")
    print("- Medical advice needs balance of engagement and accuracy")
    print("- User trust depends on appropriate response tone")
    
    print("\n🔄 NEXT CONCEPTS TO IMPLEMENT:")
    print("- One Shot Prompting (providing examples)")
    print("- Function Calling (dynamic advice)")
    print("- Top P and Top K (alternative creativity controls)")

if __name__ == "__main__":
    main()