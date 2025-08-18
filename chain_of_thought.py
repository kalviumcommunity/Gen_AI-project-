"""
LaughRx - Chain of Thought Implementation
========================================

Chain of Thought (CoT) prompting enables the AI to show its reasoning process
step-by-step, leading to more accurate and explainable medical advice.

For LaughRx, this enables:
1. Transparent medical reasoning that users can follow
2. Better handling of complex, multi-symptom scenarios
3. Step-by-step differential diagnosis consideration
4. Explainable AI decisions for medical advice
5. More accurate symptom analysis through structured thinking
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ReasoningStep(Enum):
    """Types of reasoning steps in medical analysis"""
    SYMPTOM_IDENTIFICATION = "symptom_identification"
    SEVERITY_ASSESSMENT = "severity_assessment"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    RISK_EVALUATION = "risk_evaluation"
    TREATMENT_CONSIDERATION = "treatment_consideration"
    LIFESTYLE_ANALYSIS = "lifestyle_analysis"
    FOLLOW_UP_PLANNING = "follow_up_planning"

@dataclass
class ThoughtStep:
    """Structure for individual reasoning steps"""
    step_number: int
    step_type: ReasoningStep
    thought: str
    reasoning: str
    conclusion: str

class LaughRxChainOfThought:
    def __init__(self):
        self.reasoning_templates = self._create_reasoning_templates()
        self.system_prompt = self._create_chain_of_thought_system_prompt()
    
    def _create_chain_of_thought_system_prompt(self) -> str:
        """
        Creates system prompt that enables chain of thought reasoning
        """
        return """You are LaughRx, the AI Roast Doctor. When analyzing symptoms, you must show your reasoning process step-by-step.

CHAIN OF THOUGHT STRUCTURE:
Always think through problems using these steps:

🧠 THINKING PROCESS:
Step 1: Identify and categorize all symptoms mentioned
Step 2: Assess severity and urgency of each symptom
Step 3: Consider possible causes (differential diagnosis)
Step 4: Evaluate risk factors and red flags
Step 5: Determine appropriate treatment/advice level
Step 6: Consider lifestyle factors and modifications
Step 7: Plan follow-up and monitoring needs

For each step, explain your reasoning clearly, then provide your final response.

RESPONSE FORMAT:
🧠 CHAIN OF THOUGHT:
[Show your step-by-step reasoning here]

🎭 ROAST: [Your humorous observation based on the analysis]
🔍 DIAGNOSIS: [Your medical explanation based on reasoning]
💡 ADVICE: [Your recommendations based on the thought process]

REASONING GUIDELINES:
- Be transparent about your thought process
- Consider multiple possibilities before concluding
- Explain why you ruled out certain conditions
- Show how you arrived at your advice
- Acknowledge uncertainty when appropriate
- Use medical knowledge systematically"""

    def _create_reasoning_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Creates templates for different types of medical reasoning
        """
        return {
            "simple_symptom": {
                "steps": [
                    "Identify the primary symptom and any associated symptoms",
                    "Assess severity using pain scale, duration, and impact on daily life",
                    "Consider most common causes for this symptom in general population",
                    "Evaluate any red flags that would require immediate attention",
                    "Determine if self-care is appropriate or medical consultation needed",
                    "Consider lifestyle factors that might be contributing",
                    "Recommend monitoring and follow-up timeline"
                ],
                "example": "headache analysis"
            },
            
            "complex_multi_symptom": {
                "steps": [
                    "List all symptoms and group related ones together",
                    "Identify the most concerning symptom and assess overall severity",
                    "Consider symptom patterns and how they might be connected",
                    "Think through body systems that could cause this combination",
                    "Evaluate for emergency conditions that present with these symptoms",
                    "Consider both physical and psychological contributing factors",
                    "Prioritize recommendations based on most likely causes"
                ],
                "example": "fatigue + headache + nausea analysis"
            },
            
            "lifestyle_related": {
                "steps": [
                    "Identify symptoms and their relationship to daily activities",
                    "Assess how lifestyle factors might be contributing",
                    "Consider the timeline of symptoms relative to lifestyle changes",
                    "Evaluate the severity and impact on quality of life",
                    "Think through which lifestyle modifications would be most effective",
                    "Consider barriers to lifestyle changes and realistic goals",
                    "Plan a step-by-step approach to improvement"
                ],
                "example": "work-related back pain analysis"
            },
            
            "emergency_assessment": {
                "steps": [
                    "Immediately identify any life-threatening symptoms",
                    "Assess vital signs and consciousness level if available",
                    "Consider time-sensitive conditions (stroke, heart attack, etc.)",
                    "Evaluate need for immediate emergency services",
                    "If not immediately life-threatening, assess urgency level",
                    "Consider what information would help emergency responders",
                    "Provide clear action steps prioritized by urgency"
                ],
                "example": "chest pain analysis"
            },
            
            "wellness_optimization": {
                "steps": [
                    "Understand the person's current health status and goals",
                    "Assess current lifestyle patterns and habits",
                    "Identify areas with the highest impact potential",
                    "Consider the person's readiness and capacity for change",
                    "Think through evidence-based interventions for their goals",
                    "Plan a realistic, sustainable approach to improvement",
                    "Consider how to track progress and adjust the plan"
                ],
                "example": "general health improvement analysis"
            }
        }
    
    def generate_chain_of_thought(self, symptoms: str, user_context: Dict[str, Any] = None, 
                                reasoning_type: str = "simple_symptom") -> Dict[str, Any]:
        """
        Generates a complete chain of thought analysis for given symptoms
        """
        template = self.reasoning_templates.get(reasoning_type, self.reasoning_templates["simple_symptom"])
        
        # Analyze the symptoms to determine reasoning steps
        thought_steps = self._analyze_symptoms_step_by_step(symptoms, user_context, template["steps"])
        
        # Generate the final response based on reasoning
        final_response = self._generate_response_from_reasoning(symptoms, thought_steps, user_context)
        
        return {
            "reasoning_type": reasoning_type,
            "thought_process": thought_steps,
            "final_response": final_response,
            "reasoning_quality": self._assess_reasoning_quality(thought_steps)
        }
    
    def _analyze_symptoms_step_by_step(self, symptoms: str, user_context: Dict[str, Any], 
                                     reasoning_steps: List[str]) -> List[ThoughtStep]:
        """
        Performs step-by-step analysis of symptoms
        """
        symptoms_lower = symptoms.lower()
        thought_steps = []
        
        for i, step_description in enumerate(reasoning_steps, 1):
            if i == 1:  # Symptom identification
                thought_step = self._step_1_identify_symptoms(symptoms, user_context)
            elif i == 2:  # Severity assessment
                thought_step = self._step_2_assess_severity(symptoms, user_context)
            elif i == 3:  # Differential diagnosis
                thought_step = self._step_3_differential_diagnosis(symptoms, user_context)
            elif i == 4:  # Risk evaluation
                thought_step = self._step_4_risk_evaluation(symptoms, user_context)
            elif i == 5:  # Treatment consideration
                thought_step = self._step_5_treatment_consideration(symptoms, user_context)
            elif i == 6:  # Lifestyle analysis
                thought_step = self._step_6_lifestyle_analysis(symptoms, user_context)
            elif i == 7:  # Follow-up planning
                thought_step = self._step_7_follow_up_planning(symptoms, user_context)
            else:
                thought_step = ThoughtStep(
                    step_number=i,
                    step_type=ReasoningStep.SYMPTOM_IDENTIFICATION,
                    thought=step_description,
                    reasoning="Additional analysis step",
                    conclusion="Continuing systematic evaluation"
                )
            
            thought_steps.append(thought_step)
        
        return thought_steps
    
    def _step_1_identify_symptoms(self, symptoms: str, user_context: Dict[str, Any]) -> ThoughtStep:
        """Step 1: Identify and categorize symptoms"""
        symptoms_lower = symptoms.lower()
        
        # Identify primary symptoms
        primary_symptoms = []
        if "headache" in symptoms_lower:
            primary_symptoms.append("headache")
        if "pain" in symptoms_lower:
            primary_symptoms.append("pain")
        if "tired" in symptoms_lower or "fatigue" in symptoms_lower:
            primary_symptoms.append("fatigue")
        if "nausea" in symptoms_lower:
            primary_symptoms.append("nausea")
        if "dizzy" in symptoms_lower:
            primary_symptoms.append("dizziness")
        
        # Identify associated symptoms
        associated_symptoms = []
        if "stress" in symptoms_lower:
            associated_symptoms.append("stress")
        if "sleep" in symptoms_lower:
            associated_symptoms.append("sleep issues")
        
        thought = f"Patient reports: {symptoms}"
        reasoning = f"Primary symptoms identified: {', '.join(primary_symptoms) if primary_symptoms else 'general complaint'}. Associated factors: {', '.join(associated_symptoms) if associated_symptoms else 'none specified'}."
        conclusion = f"This appears to be a {len(primary_symptoms)}-symptom presentation with {'lifestyle factors' if associated_symptoms else 'no obvious triggers mentioned'}."
        
        return ThoughtStep(
            step_number=1,
            step_type=ReasoningStep.SYMPTOM_IDENTIFICATION,
            thought=thought,
            reasoning=reasoning,
            conclusion=conclusion
        )
    
    def _step_2_assess_severity(self, symptoms: str, user_context: Dict[str, Any]) -> ThoughtStep:
        """Step 2: Assess severity and urgency"""
        symptoms_lower = symptoms.lower()
        
        severity_indicators = {
            "mild": ["slight", "minor", "little", "sometimes"],
            "moderate": ["headache", "tired", "sore", "uncomfortable"],
            "severe": ["severe", "intense", "unbearable", "can't", "unable"],
            "emergency": ["chest pain", "difficulty breathing", "loss of consciousness"]
        }
        
        severity_level = "mild"
        for level, indicators in severity_indicators.items():
            if any(indicator in symptoms_lower for indicator in indicators):
                severity_level = level
        
        thought = f"Evaluating symptom severity and urgency"
        reasoning = f"Based on language used ('{symptoms}'), this appears to be {severity_level} severity. No immediate red flags for emergency conditions detected."
        conclusion = f"Severity assessment: {severity_level}. {'Immediate medical attention needed' if severity_level == 'emergency' else 'Can proceed with systematic evaluation'}."
        
        return ThoughtStep(
            step_number=2,
            step_type=ReasoningStep.SEVERITY_ASSESSMENT,
            thought=thought,
            reasoning=reasoning,
            conclusion=conclusion
        )
    
    def _step_3_differential_diagnosis(self, symptoms: str, user_context: Dict[str, Any]) -> ThoughtStep:
        """Step 3: Consider possible causes"""
        symptoms_lower = symptoms.lower()
        
        possible_causes = []
        
        if "headache" in symptoms_lower:
            possible_causes.extend(["tension headache", "dehydration", "eye strain", "stress"])
        if "tired" in symptoms_lower or "fatigue" in symptoms_lower:
            possible_causes.extend(["poor sleep", "dehydration", "stress", "low iron"])
        if "back pain" in symptoms_lower or "posture" in symptoms_lower:
            possible_causes.extend(["muscle strain", "poor posture", "sedentary lifestyle"])
        if "stomach" in symptoms_lower or "nausea" in symptoms_lower:
            possible_causes.extend(["dietary issues", "stress", "viral infection"])
        
        # Consider context
        if user_context:
            if user_context.get("job") == "desk job" or "computer" in str(user_context).lower():
                possible_causes.append("occupational factors")
            if "stress" in str(user_context).lower():
                possible_causes.append("stress-related")
        
        thought = "Considering most likely causes for this symptom pattern"
        reasoning = f"Given the symptoms and context, possible causes include: {', '.join(possible_causes[:4]) if possible_causes else 'general lifestyle factors'}."
        conclusion = f"Most likely cause appears to be {possible_causes[0] if possible_causes else 'lifestyle-related'}, but will consider other possibilities."
        
        return ThoughtStep(
            step_number=3,
            step_type=ReasoningStep.DIFFERENTIAL_DIAGNOSIS,
            thought=thought,
            reasoning=reasoning,
            conclusion=conclusion
        )
    
    def _step_4_risk_evaluation(self, symptoms: str, user_context: Dict[str, Any]) -> ThoughtStep:
        """Step 4: Evaluate risk factors and red flags"""
        symptoms_lower = symptoms.lower()
        
        red_flags = []
        risk_factors = []
        
        # Check for red flags
        if "chest pain" in symptoms_lower:
            red_flags.append("cardiac symptoms")
        if "severe headache" in symptoms_lower:
            red_flags.append("neurological concern")
        if "difficulty breathing" in symptoms_lower:
            red_flags.append("respiratory distress")
        
        # Check for risk factors
        if user_context:
            age = user_context.get("age")
            if age and age > 50:
                risk_factors.append("age-related considerations")
            if "medication" in str(user_context).lower():
                risk_factors.append("medication interactions")
        
        thought = "Evaluating for red flags and risk factors"
        reasoning = f"Red flags identified: {', '.join(red_flags) if red_flags else 'none'}. Risk factors: {', '.join(risk_factors) if risk_factors else 'minimal'}."
        conclusion = f"Risk level: {'HIGH - immediate attention needed' if red_flags else 'LOW - can proceed with conservative management'}."
        
        return ThoughtStep(
            step_number=4,
            step_type=ReasoningStep.RISK_EVALUATION,
            thought=thought,
            reasoning=reasoning,
            conclusion=conclusion
        )
    
    def _step_5_treatment_consideration(self, symptoms: str, user_context: Dict[str, Any]) -> ThoughtStep:
        """Step 5: Determine appropriate treatment level"""
        symptoms_lower = symptoms.lower()
        
        treatment_level = "self_care"
        
        if "severe" in symptoms_lower or "chest pain" in symptoms_lower:
            treatment_level = "emergency"
        elif "persistent" in symptoms_lower or "weeks" in symptoms_lower:
            treatment_level = "medical_consultation"
        elif "headache" in symptoms_lower or "tired" in symptoms_lower:
            treatment_level = "self_care"
        
        treatment_options = {
            "self_care": ["rest", "hydration", "lifestyle modifications"],
            "medical_consultation": ["see healthcare provider", "monitoring", "possible tests"],
            "emergency": ["immediate medical attention", "emergency services"]
        }
        
        thought = "Determining appropriate level of treatment"
        reasoning = f"Based on severity and risk assessment, this requires {treatment_level.replace('_', ' ')} level intervention."
        conclusion = f"Treatment approach: {', '.join(treatment_options[treatment_level])}."
        
        return ThoughtStep(
            step_number=5,
            step_type=ReasoningStep.TREATMENT_CONSIDERATION,
            thought=thought,
            reasoning=reasoning,
            conclusion=conclusion
        )
    
    def _step_6_lifestyle_analysis(self, symptoms: str, user_context: Dict[str, Any]) -> ThoughtStep:
        """Step 6: Consider lifestyle factors"""
        symptoms_lower = symptoms.lower()
        
        lifestyle_factors = []
        recommendations = []
        
        if "headache" in symptoms_lower:
            lifestyle_factors.extend(["screen time", "hydration", "sleep"])
            recommendations.extend(["reduce screen time", "increase water intake", "improve sleep hygiene"])
        
        if "back pain" in symptoms_lower or "posture" in symptoms_lower:
            lifestyle_factors.extend(["posture", "exercise", "ergonomics"])
            recommendations.extend(["improve posture", "regular movement", "ergonomic setup"])
        
        if "tired" in symptoms_lower:
            lifestyle_factors.extend(["sleep quality", "stress", "nutrition"])
            recommendations.extend(["sleep schedule", "stress management", "balanced diet"])
        
        thought = "Analyzing lifestyle contributing factors"
        reasoning = f"Key lifestyle factors likely contributing: {', '.join(lifestyle_factors[:3]) if lifestyle_factors else 'general wellness'}."
        conclusion = f"Lifestyle modifications recommended: {', '.join(recommendations[:3]) if recommendations else 'general health maintenance'}."
        
        return ThoughtStep(
            step_number=6,
            step_type=ReasoningStep.LIFESTYLE_ANALYSIS,
            thought=thought,
            reasoning=reasoning,
            conclusion=conclusion
        )
    
    def _step_7_follow_up_planning(self, symptoms: str, user_context: Dict[str, Any]) -> ThoughtStep:
        """Step 7: Plan follow-up and monitoring"""
        symptoms_lower = symptoms.lower()
        
        follow_up_timeline = "1-2 weeks"
        monitoring_points = ["symptom improvement", "new symptoms", "response to treatment"]
        
        if "severe" in symptoms_lower:
            follow_up_timeline = "24-48 hours"
            monitoring_points = ["symptom progression", "emergency signs", "treatment response"]
        elif "chronic" in symptoms_lower or "weeks" in symptoms_lower:
            follow_up_timeline = "2-4 weeks"
            monitoring_points = ["gradual improvement", "lifestyle changes", "need for specialist"]
        
        thought = "Planning follow-up and monitoring strategy"
        reasoning = f"Given the nature of symptoms, follow-up should occur in {follow_up_timeline}."
        conclusion = f"Monitor for: {', '.join(monitoring_points)}. Seek medical attention if symptoms worsen or new concerning symptoms develop."
        
        return ThoughtStep(
            step_number=7,
            step_type=ReasoningStep.FOLLOW_UP_PLANNING,
            thought=thought,
            reasoning=reasoning,
            conclusion=conclusion
        )
    
    def _generate_response_from_reasoning(self, symptoms: str, thought_steps: List[ThoughtStep], 
                                        user_context: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates the final LaughRx response based on the reasoning process
        """
        # Extract key insights from reasoning
        primary_cause = "lifestyle factors"
        severity = "moderate"
        treatment_approach = "self-care with monitoring"
        
        for step in thought_steps:
            if step.step_type == ReasoningStep.DIFFERENTIAL_DIAGNOSIS:
                if "tension headache" in step.reasoning:
                    primary_cause = "tension headache"
                elif "dehydration" in step.reasoning:
                    primary_cause = "dehydration"
            elif step.step_type == ReasoningStep.SEVERITY_ASSESSMENT:
                if "severe" in step.conclusion:
                    severity = "severe"
                elif "mild" in step.conclusion:
                    severity = "mild"
        
        # Generate roast based on reasoning
        roast = self._generate_reasoning_based_roast(symptoms, primary_cause, user_context)
        
        # Generate diagnosis based on reasoning
        diagnosis = self._generate_reasoning_based_diagnosis(primary_cause, severity)
        
        # Generate advice based on reasoning
        advice = self._generate_reasoning_based_advice(thought_steps, treatment_approach)
        
        return {
            "roast": roast,
            "diagnosis": diagnosis,
            "advice": advice
        }
    
    def _generate_reasoning_based_roast(self, symptoms: str, primary_cause: str, 
                                      user_context: Dict[str, Any]) -> str:
        """Generate roast based on reasoning conclusions"""
        if "dehydration" in primary_cause:
            return "Let me guess - you've been treating water like it's optional while your body sends increasingly desperate signals? Your cells are probably staging a hydration protest right about now! 💧"
        elif "tension headache" in primary_cause:
            return "Ah, the classic 'my head is in a vice grip' situation! I bet you've been best friends with stress and screens while treating relaxation like a foreign concept. Your neck muscles are probably tighter than your schedule! 🤯"
        elif "posture" in primary_cause:
            return "Congratulations on your successful evolution into a human question mark! Your spine has probably forgotten what 'straight' means after all that quality time with your desk. 🦐"
        else:
            return "Your body is clearly trying to send you a message, but you've been too busy to RSVP to its complaints! Time to start listening to what it's been trying to tell you. 📢"
    
    def _generate_reasoning_based_diagnosis(self, primary_cause: str, severity: str) -> str:
        """Generate diagnosis based on reasoning"""
        if "dehydration" in primary_cause:
            return f"Based on my analysis, this appears to be {severity} dehydration with possible electrolyte imbalance affecting your overall well-being."
        elif "tension headache" in primary_cause:
            return f"My reasoning points to a {severity} tension-type headache, likely caused by muscle tension and stress-related factors."
        elif "posture" in primary_cause:
            return f"This appears to be {severity} postural strain affecting your musculoskeletal system from prolonged poor positioning."
        else:
            return f"My step-by-step analysis suggests {severity} symptoms likely related to lifestyle factors requiring attention."
    
    def _generate_reasoning_based_advice(self, thought_steps: List[ThoughtStep], 
                                       treatment_approach: str) -> str:
        """Generate advice based on reasoning steps"""
        advice_parts = []
        
        # Extract recommendations from lifestyle analysis
        for step in thought_steps:
            if step.step_type == ReasoningStep.LIFESTYLE_ANALYSIS:
                if "hydration" in step.conclusion:
                    advice_parts.append("increase your water intake")
                if "posture" in step.conclusion:
                    advice_parts.append("improve your posture and take regular breaks")
                if "sleep" in step.conclusion:
                    advice_parts.append("optimize your sleep hygiene")
                if "stress" in step.conclusion:
                    advice_parts.append("implement stress management techniques")
        
        # Extract follow-up from planning step
        follow_up = "monitor your symptoms and consult a healthcare professional if they persist or worsen"
        for step in thought_steps:
            if step.step_type == ReasoningStep.FOLLOW_UP_PLANNING:
                if "24-48 hours" in step.reasoning:
                    follow_up = "seek medical attention within 24-48 hours if symptoms don't improve"
        
        if advice_parts:
            return f"Based on my reasoning, I recommend you {', '.join(advice_parts[:3])}. Most importantly, {follow_up}."
        else:
            return f"My analysis suggests focusing on general wellness improvements and lifestyle modifications. Please {follow_up}."
    
    def _assess_reasoning_quality(self, thought_steps: List[ThoughtStep]) -> Dict[str, Any]:
        """
        Assesses the quality and completeness of the reasoning process
        """
        completeness_score = len(thought_steps) / 7 * 100  # 7 is ideal number of steps
        
        step_types_covered = set(step.step_type for step in thought_steps)
        coverage_score = len(step_types_covered) / len(ReasoningStep) * 100
        
        return {
            "completeness_score": min(completeness_score, 100),
            "coverage_score": coverage_score,
            "total_steps": len(thought_steps),
            "reasoning_depth": "thorough" if len(thought_steps) >= 6 else "basic",
            "quality_rating": "high" if completeness_score >= 80 else "moderate"
        }
    
    def create_chain_of_thought_prompt(self, symptoms: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Creates a complete chain of thought prompt for given symptoms
        """
        # Determine the best reasoning type
        reasoning_type = self._determine_reasoning_type(symptoms, user_context)
        
        # Generate the chain of thought
        cot_analysis = self.generate_chain_of_thought(symptoms, user_context, reasoning_type)
        
        # Format the thought process for the prompt
        thought_process_text = self._format_thought_process(cot_analysis["thought_process"])
        
        user_prompt = f"USER: {symptoms}"
        if user_context:
            context_parts = [f"{k}: {v}" for k, v in user_context.items()]
            user_prompt += f"\nContext: {', '.join(context_parts)}"
        
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": user_prompt,
            "chain_of_thought": thought_process_text,
            "reasoning_type": reasoning_type,
            "final_response": cot_analysis["final_response"],
            "quality_assessment": cot_analysis["reasoning_quality"]
        }
    
    def _determine_reasoning_type(self, symptoms: str, user_context: Dict[str, Any]) -> str:
        """
        Determines the most appropriate reasoning template
        """
        symptoms_lower = symptoms.lower()
        
        # Check for emergency symptoms
        emergency_keywords = ["chest pain", "difficulty breathing", "severe", "can't breathe"]
        if any(keyword in symptoms_lower for keyword in emergency_keywords):
            return "emergency_assessment"
        
        # Check for multiple symptoms
        symptom_count = len([word for word in ["headache", "pain", "tired", "nausea", "dizzy"] 
                           if word in symptoms_lower])
        if symptom_count >= 2:
            return "complex_multi_symptom"
        
        # Check for lifestyle-related issues
        lifestyle_keywords = ["work", "desk", "computer", "stress", "sleep", "posture"]
        if any(keyword in symptoms_lower for keyword in lifestyle_keywords):
            return "lifestyle_related"
        
        # Check for wellness optimization
        wellness_keywords = ["improve", "better", "healthy", "prevent", "optimize"]
        if any(keyword in symptoms_lower for keyword in wellness_keywords):
            return "wellness_optimization"
        
        return "simple_symptom"
    
    def _format_thought_process(self, thought_steps: List[ThoughtStep]) -> str:
        """
        Formats the thought process for display
        """
        formatted_text = "🧠 CHAIN OF THOUGHT:\n"
        
        for step in thought_steps:
            formatted_text += f"\nStep {step.step_number}: {step.thought}\n"
            formatted_text += f"Reasoning: {step.reasoning}\n"
            formatted_text += f"Conclusion: {step.conclusion}\n"
        
        return formatted_text
    
    def demonstrate_chain_of_thought(self):
        """
        Demonstrates chain of thought reasoning with various examples
        """
        print("🎯 LaughRx - Chain of Thought Demo")
        print("=" * 60)
        print("Chain of Thought = Step-by-step reasoning for better medical analysis!")
        print("=" * 60)
        
        # Show reasoning templates
        print("\n🧠 REASONING TEMPLATES:")
        print("-" * 50)
        
        for template_name, template_data in self.reasoning_templates.items():
            print(f"\n📋 {template_name.upper().replace('_', ' ')}:")
            print(f"   Example: {template_data['example']}")
            print(f"   Steps: {len(template_data['steps'])}")
            print(f"   Purpose: Systematic analysis for {template_name.replace('_', ' ')} scenarios")
        
        # Demonstrate reasoning process
        print(f"\n🧪 CHAIN OF THOUGHT DEMONSTRATION:")
        print("-" * 50)
        
        # Example 1: Simple symptom
        print(f"\n🔍 EXAMPLE 1: Simple Symptom Analysis")
        cot_result = self.generate_chain_of_thought("I have a headache", None, "simple_symptom")
        print(f"   Symptom: 'I have a headache'")
        print(f"   Reasoning Steps: {len(cot_result['thought_process'])}")
        print(f"   Quality: {cot_result['reasoning_quality']['quality_rating']}")
        print(f"   Final Diagnosis: {cot_result['final_response']['diagnosis'][:100]}...")
        
        # Example 2: Complex multi-symptom
        print(f"\n🔍 EXAMPLE 2: Complex Multi-Symptom Analysis")
        cot_result2 = self.generate_chain_of_thought("I have a headache, feel tired, and nauseous", 
                                                   {"age": 30, "job": "software developer"}, 
                                                   "complex_multi_symptom")
        print(f"   Symptoms: 'headache, tired, nauseous'")
        print(f"   Context: 30-year-old software developer")
        print(f"   Reasoning Steps: {len(cot_result2['thought_process'])}")
        print(f"   Quality: {cot_result2['reasoning_quality']['quality_rating']}")
        
        # Show detailed reasoning for one example
        print(f"\n🧠 DETAILED REASONING EXAMPLE:")
        print("-" * 50)
        
        sample_steps = cot_result['thought_process'][:3]  # Show first 3 steps
        for step in sample_steps:
            print(f"\n   Step {step.step_number}: {step.step_type.value}")
            print(f"   Thought: {step.thought}")
            print(f"   Reasoning: {step.reasoning}")
            print(f"   Conclusion: {step.conclusion}")

def main():
    """
    Main function to demonstrate chain of thought reasoning
    """
    cot_system = LaughRxChainOfThought()
    cot_system.demonstrate_chain_of_thought()
    
    print("\n" + "=" * 60)
    print("🎯 CHAIN OF THOUGHT - KEY BENEFITS:")
    print("=" * 60)
    print("✅ Transparent Reasoning: Users can follow the AI's thought process")
    print("✅ Better Accuracy: Step-by-step analysis reduces errors")
    print("✅ Explainable AI: Clear reasoning for medical recommendations")
    print("✅ Complex Problem Solving: Handles multi-symptom scenarios systematically")
    print("✅ Quality Assessment: Built-in evaluation of reasoning completeness")
    
    print("\n🔬 REASONING TYPES:")
    print("• Simple Symptom: Single symptom systematic analysis")
    print("• Complex Multi-Symptom: Multiple related symptoms")
    print("• Lifestyle Related: Work/lifestyle contributing factors")
    print("• Emergency Assessment: Time-critical medical situations")
    print("• Wellness Optimization: Health improvement planning")
    
    print("\n🧠 7-STEP REASONING PROCESS:")
    print("1. Symptom Identification: Categorize all symptoms")
    print("2. Severity Assessment: Evaluate urgency and intensity")
    print("3. Differential Diagnosis: Consider possible causes")
    print("4. Risk Evaluation: Identify red flags and risk factors")
    print("5. Treatment Consideration: Determine appropriate care level")
    print("6. Lifestyle Analysis: Consider contributing factors")
    print("7. Follow-up Planning: Monitor and next steps")
    
    print("\n🔄 FINAL CONCEPT TO IMPLEMENT:")
    print("- Tokens & Tokenization (understanding AI input/output limits)")

if __name__ == "__main__":
    main()