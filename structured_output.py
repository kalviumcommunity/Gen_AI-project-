"""
LaughRx - Structured Output Implementation
=========================================

Structured Output ensures the AI returns responses in a consistent JSON format
that your frontend can reliably parse and display.

This is crucial for LaughRx because:
1. Frontend needs predictable data structure
2. Easy to separate roast, diagnosis, and advice
3. Can add metadata like confidence scores, severity levels
4. Enables better error handling and validation
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SeverityLevel(Enum):
    """Enum for symptom severity levels"""
    LOW = "low"
    MODERATE = "moderate" 
    HIGH = "high"
    URGENT = "urgent"

class ResponseType(Enum):
    """Enum for response types"""
    ROAST_AND_ADVICE = "roast_and_advice"
    SERIOUS_CONCERN = "serious_concern"
    WELLNESS_TIP = "wellness_tip"
    EMERGENCY_REDIRECT = "emergency_redirect"

@dataclass
class LaughRxResponse:
    """
    Structured data class for LaughRx responses
    This ensures consistent output format
    """
    roast: str
    diagnosis: str
    advice: str
    severity: SeverityLevel
    response_type: ResponseType
    confidence_score: float  # 0.0 to 1.0
    tags: List[str]
    medical_disclaimer: str
    follow_up_questions: Optional[List[str]] = None
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        data = asdict(self)
        # Convert enums to their values
        data['severity'] = self.severity.value
        data['response_type'] = self.response_type.value
        return json.dumps(data, indent=2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['severity'] = self.severity.value
        data['response_type'] = self.response_type.value
        return data

class LaughRxStructuredOutput:
    def __init__(self):
        self.system_prompt = self._create_structured_system_prompt()
        self.medical_disclaimer = "This is for entertainment purposes only. Always consult a healthcare professional for medical concerns."
    
    def _create_structured_system_prompt(self) -> str:
        """
        Creates a system prompt that enforces structured JSON output
        """
        return """You are LaughRx, the AI Roast Doctor. You must ALWAYS respond with a valid JSON object in this exact format:

{
  "roast": "Your witty, playful roast about their lifestyle or symptoms (2-3 sentences)",
  "diagnosis": "Possible explanation for symptoms in accessible language (1-2 sentences)", 
  "advice": "Practical, actionable health advice (2-4 sentences)",
  "severity": "low|moderate|high|urgent",
  "response_type": "roast_and_advice|serious_concern|wellness_tip|emergency_redirect",
  "confidence_score": 0.85,
  "tags": ["headache", "screen_time", "dehydration"],
  "medical_disclaimer": "This is for entertainment purposes only. Always consult a healthcare professional for medical concerns.",
  "follow_up_questions": ["How long have you had this headache?", "Are you drinking enough water?"]
}

SEVERITY LEVELS:
- "low": Minor issues, lifestyle-related
- "moderate": Noticeable symptoms, needs attention
- "high": Concerning symptoms, should see doctor soon
- "urgent": Serious symptoms, seek immediate medical care

RESPONSE TYPES:
- "roast_and_advice": Normal LaughRx humor + advice
- "serious_concern": Less humor, more medical focus
- "wellness_tip": General health advice
- "emergency_redirect": Immediate medical attention needed

ROAST GUIDELINES:
- Be witty but never mean
- Connect to lifestyle choices
- Use emojis sparingly
- Keep it light and encouraging

ALWAYS return valid JSON. No additional text outside the JSON object."""

    def create_structured_prompt(self, symptoms: str, user_context: Dict[str, Any] = None) -> str:
        """
        Creates user prompt that requests structured output
        """
        prompt = f"Symptoms: {symptoms}"
        
        if user_context:
            context_parts = []
            for key, value in user_context.items():
                context_parts.append(f"{key}: {value}")
            prompt += f"\nContext: {', '.join(context_parts)}"
        
        prompt += "\n\nPlease respond with a JSON object following the LaughRx format."
        return prompt
    
    def parse_ai_response(self, ai_response: str) -> LaughRxResponse:
        """
        Parses AI response and converts to structured LaughRxResponse object
        """
        try:
            # Clean the response (remove any non-JSON text)
            cleaned_response = self._extract_json_from_response(ai_response)
            data = json.loads(cleaned_response)
            
            # Validate required fields
            required_fields = ['roast', 'diagnosis', 'advice', 'severity', 'response_type', 'confidence_score', 'tags']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create structured response
            return LaughRxResponse(
                roast=data['roast'],
                diagnosis=data['diagnosis'],
                advice=data['advice'],
                severity=SeverityLevel(data['severity']),
                response_type=ResponseType(data['response_type']),
                confidence_score=float(data['confidence_score']),
                tags=data['tags'],
                medical_disclaimer=data.get('medical_disclaimer', self.medical_disclaimer),
                follow_up_questions=data.get('follow_up_questions')
            )
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Fallback response if parsing fails
            return self._create_fallback_response(str(e))
    
    def _extract_json_from_response(self, response: str) -> str:
        """
        Extracts JSON object from AI response (handles cases where AI adds extra text)
        """
        # Find the first { and last }
        start = response.find('{')
        end = response.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            return response[start:end+1]
        else:
            raise ValueError("No valid JSON object found in response")
    
    def _create_fallback_response(self, error_msg: str) -> LaughRxResponse:
        """
        Creates a fallback response when parsing fails
        """
        return LaughRxResponse(
            roast="Oops! My roast circuits are having a moment - but I'm still here to help! 🤖",
            diagnosis="I'm having trouble processing your symptoms in my usual witty way.",
            advice="Please try rephrasing your symptoms, and I'll give you a proper LaughRx response. If this persists, consult a healthcare professional.",
            severity=SeverityLevel.LOW,
            response_type=ResponseType.ROAST_AND_ADVICE,
            confidence_score=0.1,
            tags=["system_error", "fallback"],
            medical_disclaimer=self.medical_disclaimer,
            follow_up_questions=["Could you describe your symptoms differently?"]
        )
    
    def simulate_structured_responses(self) -> List[Dict[str, Any]]:
        """
        Simulates structured responses for different symptoms
        """
        test_cases = [
            {
                "symptoms": "I have a headache",
                "context": None,
                "simulated_response": {
                    "roast": "Let me guess - you've been staring at screens all day and water is just a distant memory? Your brain is probably staging a dehydration protest! 🖥️💧",
                    "diagnosis": "This sounds like a classic tension headache, likely caused by dehydration, eye strain, or poor posture from prolonged screen time.",
                    "advice": "Here's your prescription: drink some H2O (revolutionary concept!), take regular screen breaks using the 20-20-20 rule, and maybe step outside for fresh air. Your head will thank you!",
                    "severity": "low",
                    "response_type": "roast_and_advice",
                    "confidence_score": 0.85,
                    "tags": ["headache", "screen_time", "dehydration", "eye_strain"],
                    "medical_disclaimer": "This is for entertainment purposes only. Always consult a healthcare professional for medical concerns.",
                    "follow_up_questions": ["How long have you had this headache?", "Are you drinking enough water today?", "How many hours of screen time daily?"]
                }
            },
            {
                "symptoms": "I have chest pain and shortness of breath",
                "context": {"age": "45", "medical_history": "high blood pressure"},
                "simulated_response": {
                    "roast": "I'm going to skip my usual roast here because your symptoms need serious attention.",
                    "diagnosis": "Chest pain combined with shortness of breath, especially with your medical history, requires immediate medical evaluation.",
                    "advice": "Please seek immediate medical attention. Call emergency services or go to the nearest emergency room right now. Don't drive yourself - have someone take you or call an ambulance.",
                    "severity": "urgent",
                    "response_type": "emergency_redirect",
                    "confidence_score": 0.95,
                    "tags": ["chest_pain", "shortness_of_breath", "emergency", "cardiac_concern"],
                    "medical_disclaimer": "This is for entertainment purposes only. Always consult a healthcare professional for medical concerns.",
                    "follow_up_questions": None
                }
            },
            {
                "symptoms": "I want to start exercising but don't know where to begin",
                "context": {"age": "30", "lifestyle": "sedentary"},
                "simulated_response": {
                    "roast": "Ah, the classic 'my couch and I have become one entity' situation! Time to break up this toxic relationship and get moving! 🛋️💔",
                    "diagnosis": "You're experiencing a case of 'exercise intimidation syndrome' - totally normal for recovering couch potatoes!",
                    "advice": "Start small: 10-minute walks, take stairs instead of elevators, do bodyweight exercises during TV commercials. Build the habit first, intensity later. Your future self will thank you!",
                    "severity": "low",
                    "response_type": "wellness_tip",
                    "confidence_score": 0.90,
                    "tags": ["exercise", "fitness", "lifestyle", "beginner", "motivation"],
                    "medical_disclaimer": "This is for entertainment purposes only. Always consult a healthcare professional for medical concerns.",
                    "follow_up_questions": ["What activities did you enjoy in the past?", "How much time can you dedicate daily?", "Any physical limitations?"]
                }
            }
        ]
        
        return test_cases
    
    def demonstrate_structured_output(self):
        """
        Demonstrates structured output with various examples
        """
        print("📊 LaughRx - Structured Output Demo")
        print("=" * 60)
        print("Structured Output = Consistent JSON format for reliable frontend parsing!")
        print("=" * 60)
        
        test_cases = self.simulate_structured_responses()
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n🧪 TEST CASE {i}: {case['symptoms']}")
            print("-" * 50)
            
            # Create LaughRxResponse object
            response_data = case['simulated_response']
            structured_response = LaughRxResponse(
                roast=response_data['roast'],
                diagnosis=response_data['diagnosis'],
                advice=response_data['advice'],
                severity=SeverityLevel(response_data['severity']),
                response_type=ResponseType(response_data['response_type']),
                confidence_score=response_data['confidence_score'],
                tags=response_data['tags'],
                medical_disclaimer=response_data['medical_disclaimer'],
                follow_up_questions=response_data.get('follow_up_questions')
            )
            
            print("📝 STRUCTURED JSON OUTPUT:")
            print(structured_response.to_json())
            
            print(f"\n🎯 KEY BENEFITS:")
            print(f"- Severity Level: {structured_response.severity.value}")
            print(f"- Response Type: {structured_response.response_type.value}")
            print(f"- Confidence: {structured_response.confidence_score}")
            print(f"- Tags: {', '.join(structured_response.tags)}")

def main():
    """
    Main function to demonstrate structured output
    """
    structured_system = LaughRxStructuredOutput()
    structured_system.demonstrate_structured_output()
    
    print("\n" + "=" * 60)
    print("🎯 STRUCTURED OUTPUT - KEY BENEFITS:")
    print("=" * 60)
    print("✅ Consistent Format: Always returns the same JSON structure")
    print("✅ Easy Frontend Parsing: No need to parse unstructured text")
    print("✅ Rich Metadata: Severity, confidence, tags for better UX")
    print("✅ Error Handling: Fallback responses when parsing fails")
    print("✅ Type Safety: Enums prevent invalid values")
    print("✅ Extensible: Easy to add new fields without breaking existing code")
    
    print("\n🔬 WHY STRUCTURED OUTPUT IS ESSENTIAL:")
    print("- Frontend can reliably display roast, diagnosis, advice separately")
    print("- Severity levels enable different UI treatments")
    print("- Tags allow for symptom categorization and analytics")
    print("- Confidence scores help with response quality assessment")
    print("- Follow-up questions enable conversational flow")
    
    print("\n🔄 NEXT CONCEPTS TO IMPLEMENT:")
    print("- Temperature Control (response creativity)")
    print("- One Shot Prompting (providing examples)")
    print("- Function Calling (dynamic advice)")

if __name__ == "__main__":
    main()