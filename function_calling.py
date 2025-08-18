"""
LaughRx - Function Calling Implementation
========================================

Function Calling allows the AI to dynamically call specific functions to provide
targeted advice, look up information, or perform calculations based on user symptoms.

For LaughRx, this enables:
1. Dynamic symptom analysis and severity assessment
2. Personalized advice based on user profile (age, lifestyle, etc.)
3. Drug interaction checks and medication guidance
4. Emergency situation detection and appropriate responses
5. Lifestyle recommendation engines
"""

import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import datetime

class FunctionCategory(Enum):
    """Categories of functions available to the AI"""
    SYMPTOM_ANALYSIS = "symptom_analysis"
    LIFESTYLE_ADVICE = "lifestyle_advice"
    EMERGENCY_DETECTION = "emergency_detection"
    MEDICATION_INFO = "medication_info"
    WELLNESS_CALCULATOR = "wellness_calculator"

@dataclass
class FunctionDefinition:
    """Structure for defining callable functions"""
    name: str
    description: str
    category: FunctionCategory
    parameters: Dict[str, Any]
    required_params: List[str]
    example_call: str

class LaughRxFunctionCalling:
    def __init__(self):
        self.available_functions = self._register_functions()
        self.function_definitions = self._create_function_definitions()
        self.system_prompt = self._create_function_calling_system_prompt()
    
    def _register_functions(self) -> Dict[str, Callable]:
        """
        Register all available functions that the AI can call
        """
        return {
            "analyze_symptom_severity": self.analyze_symptom_severity,
            "get_lifestyle_recommendations": self.get_lifestyle_recommendations,
            "check_emergency_symptoms": self.check_emergency_symptoms,
            "calculate_bmi": self.calculate_bmi,
            "get_medication_interactions": self.get_medication_interactions,
            "assess_sleep_quality": self.assess_sleep_quality,
            "generate_exercise_plan": self.generate_exercise_plan,
            "check_symptom_duration": self.check_symptom_duration,
            "get_age_specific_advice": self.get_age_specific_advice,
            "calculate_hydration_needs": self.calculate_hydration_needs
        }
    
    def _create_function_definitions(self) -> List[FunctionDefinition]:
        """
        Define all functions available to the AI with their parameters
        """
        return [
            FunctionDefinition(
                name="analyze_symptom_severity",
                description="Analyzes symptom severity and urgency level",
                category=FunctionCategory.SYMPTOM_ANALYSIS,
                parameters={
                    "symptoms": {"type": "string", "description": "List of symptoms"},
                    "duration": {"type": "string", "description": "How long symptoms have lasted"},
                    "intensity": {"type": "integer", "description": "Pain/discomfort level 1-10"}
                },
                required_params=["symptoms"],
                example_call="analyze_symptom_severity(symptoms='headache, nausea', duration='2 days', intensity=7)"
            ),
            
            FunctionDefinition(
                name="get_lifestyle_recommendations",
                description="Provides personalized lifestyle advice based on user profile",
                category=FunctionCategory.LIFESTYLE_ADVICE,
                parameters={
                    "age": {"type": "integer", "description": "User's age"},
                    "activity_level": {"type": "string", "description": "sedentary, moderate, active"},
                    "health_goals": {"type": "string", "description": "User's health objectives"},
                    "current_issues": {"type": "string", "description": "Current health concerns"}
                },
                required_params=["current_issues"],
                example_call="get_lifestyle_recommendations(age=30, activity_level='sedentary', current_issues='back pain')"
            ),
            
            FunctionDefinition(
                name="check_emergency_symptoms",
                description="Detects if symptoms require immediate medical attention",
                category=FunctionCategory.EMERGENCY_DETECTION,
                parameters={
                    "symptoms": {"type": "string", "description": "Current symptoms"},
                    "vital_signs": {"type": "object", "description": "Blood pressure, heart rate, etc."}
                },
                required_params=["symptoms"],
                example_call="check_emergency_symptoms(symptoms='chest pain, shortness of breath')"
            ),
            
            FunctionDefinition(
                name="calculate_bmi",
                description="Calculates BMI and provides weight category assessment",
                category=FunctionCategory.WELLNESS_CALCULATOR,
                parameters={
                    "weight_kg": {"type": "number", "description": "Weight in kilograms"},
                    "height_cm": {"type": "number", "description": "Height in centimeters"}
                },
                required_params=["weight_kg", "height_cm"],
                example_call="calculate_bmi(weight_kg=70, height_cm=175)"
            ),
            
            FunctionDefinition(
                name="get_medication_interactions",
                description="Checks for potential medication interactions and contraindications",
                category=FunctionCategory.MEDICATION_INFO,
                parameters={
                    "current_medications": {"type": "array", "description": "List of current medications"},
                    "proposed_treatment": {"type": "string", "description": "Suggested treatment or medication"}
                },
                required_params=["current_medications"],
                example_call="get_medication_interactions(current_medications=['aspirin', 'ibuprofen'])"
            ),
            
            FunctionDefinition(
                name="assess_sleep_quality",
                description="Analyzes sleep patterns and provides improvement suggestions",
                category=FunctionCategory.LIFESTYLE_ADVICE,
                parameters={
                    "sleep_hours": {"type": "number", "description": "Average hours of sleep"},
                    "sleep_quality": {"type": "string", "description": "poor, fair, good, excellent"},
                    "bedtime": {"type": "string", "description": "Usual bedtime"},
                    "wake_time": {"type": "string", "description": "Usual wake time"}
                },
                required_params=["sleep_hours"],
                example_call="assess_sleep_quality(sleep_hours=5, sleep_quality='poor', bedtime='1 AM')"
            )
        ]
    
    def _create_function_calling_system_prompt(self) -> str:
        """
        Creates system prompt that enables function calling
        """
        functions_list = ""
        for func_def in self.function_definitions:
            functions_list += f"\n- {func_def.name}: {func_def.description}"
        
        return f"""You are LaughRx, the AI Roast Doctor with access to specialized medical functions.

AVAILABLE FUNCTIONS:
{functions_list}

FUNCTION CALLING RULES:
1. When a user describes symptoms, ALWAYS call analyze_symptom_severity first
2. For emergency symptoms, immediately call check_emergency_symptoms
3. For lifestyle issues, call get_lifestyle_recommendations
4. For weight/fitness questions, use calculate_bmi or generate_exercise_plan
5. For sleep problems, call assess_sleep_quality
6. Always use function results to enhance your roast and advice

RESPONSE STRUCTURE:
1. 🎭 ROAST: Incorporate function results into your humor
2. 🔍 DIAGNOSIS: Use function analysis for medical explanation
3. 💡 ADVICE: Base recommendations on function outputs
4. 📊 DATA: Include relevant function results

FUNCTION CALLING FORMAT:
When you need to call a function, use this format:
FUNCTION_CALL: function_name(parameter1=value1, parameter2=value2)

Remember: Use functions to provide data-driven, personalized advice while maintaining your humorous personality!"""
    
    # Function Implementations
    def analyze_symptom_severity(self, symptoms: str, duration: str = None, intensity: int = None) -> Dict[str, Any]:
        """
        Analyzes symptom severity and provides urgency assessment
        """
        symptoms_lower = symptoms.lower()
        
        # Emergency symptoms
        emergency_keywords = ['chest pain', 'difficulty breathing', 'severe headache', 'loss of consciousness', 
                            'severe bleeding', 'stroke symptoms', 'heart attack']
        
        # High severity symptoms
        high_severity = ['persistent fever', 'severe pain', 'vision changes', 'severe dizziness']
        
        # Moderate severity symptoms
        moderate_severity = ['headache', 'back pain', 'fatigue', 'nausea', 'muscle pain']
        
        severity_level = "low"
        urgency = "routine"
        recommendations = []
        
        if any(keyword in symptoms_lower for keyword in emergency_keywords):
            severity_level = "emergency"
            urgency = "immediate"
            recommendations = ["Seek immediate medical attention", "Call emergency services if severe"]
        elif any(keyword in symptoms_lower for keyword in high_severity):
            severity_level = "high"
            urgency = "urgent"
            recommendations = ["Consult healthcare provider within 24 hours", "Monitor symptoms closely"]
        elif any(keyword in symptoms_lower for keyword in moderate_severity):
            severity_level = "moderate"
            urgency = "routine"
            recommendations = ["Self-care measures appropriate", "See doctor if symptoms persist"]
        
        # Adjust based on duration and intensity
        if duration and ("weeks" in duration or "months" in duration):
            if severity_level == "low":
                severity_level = "moderate"
        
        if intensity and intensity >= 8:
            if severity_level != "emergency":
                severity_level = "high"
                urgency = "urgent"
        
        return {
            "severity_level": severity_level,
            "urgency": urgency,
            "risk_factors": self._identify_risk_factors(symptoms_lower),
            "recommendations": recommendations,
            "follow_up_needed": severity_level in ["high", "emergency"]
        }
    
    def get_lifestyle_recommendations(self, current_issues: str, age: int = None, 
                                    activity_level: str = "moderate", health_goals: str = None) -> Dict[str, Any]:
        """
        Provides personalized lifestyle recommendations
        """
        issues_lower = current_issues.lower()
        recommendations = {
            "exercise": [],
            "nutrition": [],
            "sleep": [],
            "stress_management": [],
            "specific_advice": []
        }
        
        # Exercise recommendations
        if "back pain" in issues_lower or "posture" in issues_lower:
            recommendations["exercise"] = ["Strengthen core muscles", "Improve posture", "Regular stretching"]
        elif "fatigue" in issues_lower:
            recommendations["exercise"] = ["Light cardio", "Gradual activity increase", "Avoid overexertion"]
        elif "stress" in issues_lower:
            recommendations["exercise"] = ["Yoga", "Walking", "Swimming"]
        
        # Nutrition recommendations
        if "headache" in issues_lower:
            recommendations["nutrition"] = ["Increase water intake", "Regular meals", "Limit caffeine"]
        elif "digestive" in issues_lower or "stomach" in issues_lower:
            recommendations["nutrition"] = ["Smaller frequent meals", "Avoid trigger foods", "Increase fiber"]
        
        # Age-specific adjustments
        if age:
            if age > 50:
                recommendations["specific_advice"].append("Regular health screenings recommended")
            elif age < 30:
                recommendations["specific_advice"].append("Focus on building healthy habits early")
        
        return {
            "recommendations": recommendations,
            "priority_areas": self._identify_priority_areas(issues_lower),
            "timeline": "2-4 weeks for initial improvements"
        }
    
    def check_emergency_symptoms(self, symptoms: str, vital_signs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Checks for emergency symptoms requiring immediate attention
        """
        symptoms_lower = symptoms.lower()
        
        emergency_indicators = {
            "cardiac": ["chest pain", "heart attack", "severe chest pressure"],
            "neurological": ["stroke", "severe headache", "loss of consciousness", "confusion"],
            "respiratory": ["difficulty breathing", "shortness of breath", "can't breathe"],
            "bleeding": ["severe bleeding", "heavy bleeding", "blood loss"],
            "allergic": ["severe allergic reaction", "anaphylaxis", "swelling throat"]
        }
        
        detected_emergencies = []
        for category, keywords in emergency_indicators.items():
            if any(keyword in symptoms_lower for keyword in keywords):
                detected_emergencies.append(category)
        
        is_emergency = len(detected_emergencies) > 0
        
        return {
            "is_emergency": is_emergency,
            "emergency_types": detected_emergencies,
            "immediate_actions": self._get_emergency_actions(detected_emergencies),
            "call_911": is_emergency,
            "urgency_level": "CRITICAL" if is_emergency else "NORMAL"
        }
    
    def calculate_bmi(self, weight_kg: float, height_cm: float) -> Dict[str, Any]:
        """
        Calculates BMI and provides health category assessment
        """
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            category = "Underweight"
            advice = "Consider consulting a nutritionist for healthy weight gain"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            advice = "Maintain current healthy weight through balanced diet and exercise"
        elif 25 <= bmi < 30:
            category = "Overweight"
            advice = "Consider gradual weight loss through diet and exercise"
        else:
            category = "Obese"
            advice = "Consult healthcare provider for weight management plan"
        
        return {
            "bmi": round(bmi, 1),
            "category": category,
            "health_advice": advice,
            "ideal_weight_range": f"{round(18.5 * height_m**2, 1)}-{round(24.9 * height_m**2, 1)} kg"
        }
    
    def get_medication_interactions(self, current_medications: List[str], 
                                  proposed_treatment: str = None) -> Dict[str, Any]:
        """
        Checks for potential medication interactions (simplified version)
        """
        # This is a simplified version - real implementation would use medical databases
        common_interactions = {
            "aspirin": ["warfarin", "ibuprofen", "alcohol"],
            "ibuprofen": ["aspirin", "warfarin", "blood pressure medications"],
            "acetaminophen": ["alcohol", "warfarin"],
            "caffeine": ["anxiety medications", "sleep medications"]
        }
        
        potential_interactions = []
        warnings = []
        
        for med1 in current_medications:
            med1_lower = med1.lower()
            if med1_lower in common_interactions:
                for med2 in current_medications:
                    if med2.lower() in common_interactions[med1_lower]:
                        potential_interactions.append(f"{med1} + {med2}")
        
        if potential_interactions:
            warnings.append("Potential drug interactions detected")
            warnings.append("Consult pharmacist or doctor before combining medications")
        
        return {
            "interactions_found": len(potential_interactions) > 0,
            "potential_interactions": potential_interactions,
            "warnings": warnings,
            "recommendation": "Always consult healthcare provider before starting new medications"
        }
    
    def assess_sleep_quality(self, sleep_hours: float, sleep_quality: str = "fair", 
                           bedtime: str = None, wake_time: str = None) -> Dict[str, Any]:
        """
        Analyzes sleep patterns and provides improvement suggestions
        """
        assessment = {
            "sleep_duration_rating": "good" if 7 <= sleep_hours <= 9 else "needs_improvement",
            "recommendations": [],
            "sleep_score": 0
        }
        
        # Duration scoring
        if 7 <= sleep_hours <= 9:
            assessment["sleep_score"] += 40
            assessment["recommendations"].append("Good sleep duration - maintain current schedule")
        elif sleep_hours < 7:
            assessment["recommendations"].append("Increase sleep duration to 7-9 hours")
        else:
            assessment["recommendations"].append("Consider if you need that much sleep")
        
        # Quality scoring
        quality_scores = {"poor": 10, "fair": 20, "good": 30, "excellent": 40}
        assessment["sleep_score"] += quality_scores.get(sleep_quality, 20)
        
        if sleep_quality in ["poor", "fair"]:
            assessment["recommendations"].extend([
                "Improve sleep hygiene",
                "Create consistent bedtime routine",
                "Optimize sleep environment"
            ])
        
        # Bedtime analysis
        if bedtime and "AM" in bedtime.upper():
            assessment["recommendations"].append("Consider earlier bedtime for better sleep quality")
        
        assessment["overall_rating"] = "excellent" if assessment["sleep_score"] >= 70 else \
                                     "good" if assessment["sleep_score"] >= 50 else \
                                     "needs_improvement"
        
        return assessment
    
    def generate_exercise_plan(self, fitness_level: str = "beginner", 
                             health_goals: str = "general_fitness", 
                             available_time: int = 30) -> Dict[str, Any]:
        """
        Generates personalized exercise recommendations
        """
        plans = {
            "beginner": {
                "cardio": "10-15 minutes walking",
                "strength": "Bodyweight exercises 2x/week",
                "flexibility": "5-10 minutes stretching daily"
            },
            "intermediate": {
                "cardio": "20-30 minutes moderate exercise",
                "strength": "Weight training 3x/week",
                "flexibility": "Yoga or stretching 15 minutes"
            },
            "advanced": {
                "cardio": "30-45 minutes varied intensity",
                "strength": "Progressive weight training 4x/week",
                "flexibility": "Dynamic stretching and mobility work"
            }
        }
        
        plan = plans.get(fitness_level, plans["beginner"])
        
        return {
            "weekly_plan": plan,
            "progression_timeline": "2-4 weeks per level increase",
            "safety_notes": ["Start slowly", "Listen to your body", "Consult doctor if health concerns"],
            "estimated_time": f"{available_time} minutes per session"
        }
    
    def check_symptom_duration(self, symptoms: str, duration: str) -> Dict[str, Any]:
        """
        Analyzes symptom duration and provides timeline-based advice
        """
        duration_lower = duration.lower()
        
        if "hours" in duration_lower or "today" in duration_lower:
            timeline = "acute"
            advice = "Monitor symptoms, self-care appropriate"
        elif "days" in duration_lower:
            timeline = "subacute"
            advice = "If symptoms persist beyond a week, consult healthcare provider"
        elif "weeks" in duration_lower or "months" in duration_lower:
            timeline = "chronic"
            advice = "Chronic symptoms warrant medical evaluation"
        else:
            timeline = "unclear"
            advice = "Please specify how long you've had these symptoms"
        
        return {
            "timeline_category": timeline,
            "duration_concern": timeline == "chronic",
            "advice": advice,
            "follow_up_recommended": timeline in ["subacute", "chronic"]
        }
    
    def get_age_specific_advice(self, age: int, symptoms: str) -> Dict[str, Any]:
        """
        Provides age-appropriate health advice
        """
        if age < 18:
            category = "pediatric"
            advice = "Consult pediatrician for proper evaluation"
        elif 18 <= age < 65:
            category = "adult"
            advice = "Standard adult health guidelines apply"
        else:
            category = "senior"
            advice = "Consider age-related health factors"
        
        age_specific_considerations = {
            "pediatric": ["Growth and development factors", "Dosage adjustments needed"],
            "adult": ["Lifestyle factors important", "Preventive care recommended"],
            "senior": ["Multiple medications possible", "Fall risk considerations", "Cognitive factors"]
        }
        
        return {
            "age_category": category,
            "considerations": age_specific_considerations[category],
            "advice": advice
        }
    
    def calculate_hydration_needs(self, weight_kg: float, activity_level: str = "moderate") -> Dict[str, Any]:
        """
        Calculates daily hydration needs based on weight and activity
        """
        base_water = weight_kg * 35  # ml per kg
        
        activity_multipliers = {
            "sedentary": 1.0,
            "moderate": 1.2,
            "active": 1.5,
            "very_active": 1.8
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.2)
        daily_water_ml = base_water * multiplier
        daily_water_liters = daily_water_ml / 1000
        
        return {
            "daily_water_liters": round(daily_water_liters, 1),
            "daily_water_glasses": round(daily_water_ml / 250),  # 250ml per glass
            "activity_adjustment": f"{int((multiplier - 1) * 100)}% increase for {activity_level} lifestyle",
            "hydration_tips": ["Drink water throughout the day", "Monitor urine color", "Increase intake in hot weather"]
        }
    
    # Helper methods
    def _identify_risk_factors(self, symptoms: str) -> List[str]:
        """Identifies potential risk factors from symptoms"""
        risk_factors = []
        if "chest" in symptoms:
            risk_factors.append("Cardiovascular concern")
        if "headache" in symptoms and "severe" in symptoms:
            risk_factors.append("Neurological concern")
        if "breathing" in symptoms:
            risk_factors.append("Respiratory concern")
        return risk_factors
    
    def _identify_priority_areas(self, issues: str) -> List[str]:
        """Identifies priority areas for lifestyle changes"""
        priorities = []
        if "pain" in issues:
            priorities.append("Pain management")
        if "stress" in issues:
            priorities.append("Stress reduction")
        if "sleep" in issues:
            priorities.append("Sleep hygiene")
        if "weight" in issues:
            priorities.append("Weight management")
        return priorities
    
    def _get_emergency_actions(self, emergency_types: List[str]) -> List[str]:
        """Gets immediate actions for emergency situations"""
        actions = ["Call 911 immediately"]
        if "cardiac" in emergency_types:
            actions.append("If available, take aspirin")
        if "respiratory" in emergency_types:
            actions.append("Sit upright, loosen tight clothing")
        if "allergic" in emergency_types:
            actions.append("Use EpiPen if available")
        return actions
    
    def call_function(self, function_name: str, **kwargs) -> Dict[str, Any]:
        """
        Calls a specific function with given parameters
        """
        if function_name not in self.available_functions:
            return {"error": f"Function {function_name} not found"}
        
        try:
            result = self.available_functions[function_name](**kwargs)
            return {"success": True, "result": result, "function_called": function_name}
        except Exception as e:
            return {"error": f"Error calling {function_name}: {str(e)}"}
    
    def create_function_calling_prompt(self, symptoms: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Creates a prompt that enables function calling for the given symptoms
        """
        # Determine which functions would be most useful
        suggested_functions = self._suggest_functions_for_symptoms(symptoms, user_context)
        
        user_prompt = f"USER: {symptoms}"
        if user_context:
            context_parts = [f"{k}: {v}" for k, v in user_context.items()]
            user_prompt += f"\nContext: {', '.join(context_parts)}"
        
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": user_prompt,
            "suggested_functions": suggested_functions,
            "available_functions": [func.name for func in self.function_definitions]
        }
    
    def _suggest_functions_for_symptoms(self, symptoms: str, user_context: Dict[str, Any] = None) -> List[str]:
        """
        Suggests which functions would be most useful for given symptoms
        """
        symptoms_lower = symptoms.lower()
        suggested = ["analyze_symptom_severity"]  # Always start with this
        
        # Emergency check
        emergency_keywords = ['chest pain', 'difficulty breathing', 'severe']
        if any(keyword in symptoms_lower for keyword in emergency_keywords):
            suggested.append("check_emergency_symptoms")
        
        # Lifestyle advice
        lifestyle_keywords = ['stress', 'sleep', 'tired', 'back pain', 'posture']
        if any(keyword in symptoms_lower for keyword in lifestyle_keywords):
            suggested.append("get_lifestyle_recommendations")
        
        # Sleep issues
        if 'sleep' in symptoms_lower or 'tired' in symptoms_lower:
            suggested.append("assess_sleep_quality")
        
        # Weight/BMI related
        if user_context and ('weight' in str(user_context).lower() or 'height' in str(user_context).lower()):
            suggested.append("calculate_bmi")
        
        # Medication concerns
        if 'medication' in symptoms_lower or 'drug' in symptoms_lower:
            suggested.append("get_medication_interactions")
        
        return suggested
    
    def demonstrate_function_calling(self):
        """
        Demonstrates function calling capabilities
        """
        print("🎯 LaughRx - Function Calling Demo")
        print("=" * 60)
        print("Function Calling = AI can dynamically call specialized functions!")
        print("=" * 60)
        
        # Show available functions
        print("\n🔧 AVAILABLE FUNCTIONS:")
        print("-" * 50)
        
        for category in FunctionCategory:
            category_functions = [f for f in self.function_definitions if f.category == category]
            if category_functions:
                print(f"\n📋 {category.value.upper().replace('_', ' ')}:")
                for func in category_functions:
                    print(f"   • {func.name}: {func.description}")
        
        # Demonstrate function calls
        print(f"\n🧪 FUNCTION CALL DEMONSTRATIONS:")
        print("-" * 50)
        
        # Example 1: Symptom analysis
        print(f"\n🔍 SYMPTOM ANALYSIS:")
        result1 = self.call_function("analyze_symptom_severity", 
                                   symptoms="severe headache and nausea", 
                                   duration="2 days", 
                                   intensity=8)
        print(f"   Input: severe headache, nausea (2 days, intensity 8)")
        print(f"   Result: {result1['result']['severity_level']} severity, {result1['result']['urgency']} urgency")
        
        # Example 2: BMI calculation
        print(f"\n📊 BMI CALCULATION:")
        result2 = self.call_function("calculate_bmi", weight_kg=70, height_cm=175)
        print(f"   Input: 70kg, 175cm")
        print(f"   Result: BMI {result2['result']['bmi']}, {result2['result']['category']}")
        
        # Example 3: Emergency check
        print(f"\n🚨 EMERGENCY DETECTION:")
        result3 = self.call_function("check_emergency_symptoms", 
                                   symptoms="chest pain and shortness of breath")
        print(f"   Input: chest pain and shortness of breath")
        print(f"   Result: Emergency = {result3['result']['is_emergency']}, Call 911 = {result3['result']['call_911']}")
        
        # Example 4: Sleep assessment
        print(f"\n😴 SLEEP QUALITY ASSESSMENT:")
        result4 = self.call_function("assess_sleep_quality", 
                                   sleep_hours=5, 
                                   sleep_quality="poor", 
                                   bedtime="1 AM")
        print(f"   Input: 5 hours sleep, poor quality, 1 AM bedtime")
        print(f"   Result: {result4['result']['overall_rating']} sleep quality")

def main():
    """
    Main function to demonstrate function calling
    """
    function_system = LaughRxFunctionCalling()
    function_system.demonstrate_function_calling()
    
    print("\n" + "=" * 60)
    print("🎯 FUNCTION CALLING - KEY BENEFITS:")
    print("=" * 60)
    print("✅ Dynamic Analysis: AI can perform calculations and assessments")
    print("✅ Personalized Advice: Functions use user data for custom recommendations")
    print("✅ Emergency Detection: Automatic identification of urgent situations")
    print("✅ Data-Driven Responses: Roasts and advice based on actual analysis")
    print("✅ Extensible: Easy to add new specialized functions")
    
    print("\n🔬 FUNCTION CATEGORIES:")
    print("• Symptom Analysis: Severity assessment, duration analysis")
    print("• Lifestyle Advice: Personalized recommendations based on profile")
    print("• Emergency Detection: Critical symptom identification")
    print("• Wellness Calculators: BMI, hydration needs, exercise plans")
    print("• Medication Info: Interaction checks, safety warnings")
    
    print("\n🔄 NEXT CONCEPTS TO IMPLEMENT:")
    print("- Chain of Thought (step-by-step reasoning)")
    print("- Tokens & Tokenization (understanding AI limits)")

if __name__ == "__main__":
    main()