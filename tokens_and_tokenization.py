"""
LaughRx - Tokens and Tokenization Implementation
===============================================

Tokens and Tokenization are fundamental to understanding how AI models process text.
Every AI model has token limits that affect cost, performance, and response quality.

For LaughRx, understanding tokenization helps:
1. Optimize prompt efficiency and reduce costs
2. Stay within model limits for complex medical scenarios
3. Balance detail vs. brevity in responses
4. Estimate API costs for different prompt strategies
5. Design prompts that maximize information density
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class TokenizerType(Enum):
    """Different tokenization approaches"""
    SIMPLE_WHITESPACE = "whitespace"
    WORD_BASED = "word_based"
    SUBWORD_BPE = "bpe_approximation"
    CHARACTER_BASED = "character"

@dataclass
class TokenAnalysis:
    """Structure for token analysis results"""
    text: str
    token_count: int
    tokens: List[str]
    tokenizer_type: TokenizerType
    efficiency_score: float
    cost_estimate: float

class LaughRxTokenization:
    def __init__(self):
        self.model_limits = self._define_model_limits()
        self.cost_per_token = self._define_cost_structure()
        self.optimization_strategies = self._create_optimization_strategies()
    
    def _define_model_limits(self) -> Dict[str, Dict[str, int]]:
        """
        Define token limits for popular AI models
        """
        return {
            "gpt-3.5-turbo": {
                "max_tokens": 4096,
                "context_window": 4096,
                "recommended_prompt": 3000,
                "recommended_response": 1000
            },
            "gpt-4": {
                "max_tokens": 8192,
                "context_window": 8192,
                "recommended_prompt": 6000,
                "recommended_response": 2000
            },
            "gpt-4-turbo": {
                "max_tokens": 128000,
                "context_window": 128000,
                "recommended_prompt": 100000,
                "recommended_response": 4000
            },
            "claude-3-sonnet": {
                "max_tokens": 200000,
                "context_window": 200000,
                "recommended_prompt": 150000,
                "recommended_response": 4000
            },
            "gemini-pro": {
                "max_tokens": 32768,
                "context_window": 32768,
                "recommended_prompt": 25000,
                "recommended_response": 8000
            }
        }
    
    def _define_cost_structure(self) -> Dict[str, Dict[str, float]]:
        """
        Define approximate costs per 1K tokens (as of 2024)
        """
        return {
            "gpt-3.5-turbo": {
                "input": 0.0015,  # $0.0015 per 1K input tokens
                "output": 0.002   # $0.002 per 1K output tokens
            },
            "gpt-4": {
                "input": 0.03,   # $0.03 per 1K input tokens
                "output": 0.06   # $0.06 per 1K output tokens
            },
            "gpt-4-turbo": {
                "input": 0.01,   # $0.01 per 1K input tokens
                "output": 0.03   # $0.03 per 1K output tokens
            },
            "claude-3-sonnet": {
                "input": 0.003,  # $0.003 per 1K input tokens
                "output": 0.015  # $0.015 per 1K output tokens
            },
            "gemini-pro": {
                "input": 0.00025, # $0.00025 per 1K input tokens
                "output": 0.0005  # $0.0005 per 1K output tokens
            }
        }
    
    def _create_optimization_strategies(self) -> Dict[str, Dict[str, Any]]:
        """
        Create strategies for optimizing token usage
        """
        return {
            "prompt_compression": {
                "description": "Reduce prompt length while maintaining effectiveness",
                "techniques": [
                    "Remove redundant words",
                    "Use abbreviations for common terms",
                    "Combine similar instructions",
                    "Use bullet points instead of sentences"
                ],
                "example": "Instead of 'Please provide a detailed analysis' use 'Analyze:'"
            },
            "response_optimization": {
                "description": "Guide AI to produce efficient responses",
                "techniques": [
                    "Specify desired response length",
                    "Request structured formats (JSON, bullets)",
                    "Ask for key points only",
                    "Use max_tokens parameter"
                ],
                "example": "Respond in exactly 3 bullet points, max 50 words each"
            },
            "context_management": {
                "description": "Manage conversation context efficiently",
                "techniques": [
                    "Summarize previous context",
                    "Remove irrelevant history",
                    "Use system prompts for persistent instructions",
                    "Implement sliding window for long conversations"
                ],
                "example": "Summarize last 5 exchanges instead of including full history"
            },
            "smart_chunking": {
                "description": "Break large inputs into optimal chunks",
                "techniques": [
                    "Chunk by semantic meaning",
                    "Overlap chunks for context",
                    "Process in parallel when possible",
                    "Combine results intelligently"
                ],
                "example": "Split long medical history into symptom categories"
            }
        }
    
    def tokenize_text(self, text: str, tokenizer_type: TokenizerType = TokenizerType.SUBWORD_BPE) -> TokenAnalysis:
        """
        Tokenizes text using specified tokenization method
        """
        if tokenizer_type == TokenizerType.SIMPLE_WHITESPACE:
            tokens = self._whitespace_tokenize(text)
        elif tokenizer_type == TokenizerType.WORD_BASED:
            tokens = self._word_tokenize(text)
        elif tokenizer_type == TokenizerType.SUBWORD_BPE:
            tokens = self._bpe_approximate_tokenize(text)
        elif tokenizer_type == TokenizerType.CHARACTER_BASED:
            tokens = self._character_tokenize(text)
        else:
            tokens = self._bpe_approximate_tokenize(text)  # Default
        
        token_count = len(tokens)
        efficiency_score = self._calculate_efficiency_score(text, token_count)
        cost_estimate = self._estimate_cost(token_count)
        
        return TokenAnalysis(
            text=text,
            token_count=token_count,
            tokens=tokens,
            tokenizer_type=tokenizer_type,
            efficiency_score=efficiency_score,
            cost_estimate=cost_estimate
        )
    
    def _whitespace_tokenize(self, text: str) -> List[str]:
        """Simple whitespace-based tokenization"""
        return text.split()
    
    def _word_tokenize(self, text: str) -> List[str]:
        """Word-based tokenization with punctuation handling"""
        # Split on whitespace and punctuation
        tokens = re.findall(r'\b\w+\b|[^\w\s]', text)
        return [token for token in tokens if token.strip()]
    
    def _bpe_approximate_tokenize(self, text: str) -> List[str]:
        """
        Approximates BPE (Byte Pair Encoding) tokenization used by GPT models
        This is a simplified version for demonstration
        """
        # First, do word-level split
        words = re.findall(r'\b\w+\b|[^\w\s]', text)
        tokens = []
        
        for word in words:
            if len(word) <= 3:
                tokens.append(word)
            else:
                # Simulate subword splitting for longer words
                # Real BPE is much more sophisticated
                if len(word) <= 6:
                    tokens.append(word)
                else:
                    # Split longer words into chunks (approximation)
                    chunk_size = 4
                    for i in range(0, len(word), chunk_size):
                        chunk = word[i:i+chunk_size]
                        tokens.append(chunk)
        
        return tokens
    
    def _character_tokenize(self, text: str) -> List[str]:
        """Character-based tokenization"""
        return list(text)
    
    def _calculate_efficiency_score(self, text: str, token_count: int) -> float:
        """
        Calculates efficiency score (characters per token)
        Higher score = more efficient tokenization
        """
        if token_count == 0:
            return 0.0
        return len(text) / token_count
    
    def _estimate_cost(self, token_count: int, model: str = "gpt-3.5-turbo", 
                      is_input: bool = True) -> float:
        """
        Estimates cost for given token count
        """
        if model not in self.cost_per_token:
            model = "gpt-3.5-turbo"  # Default
        
        cost_type = "input" if is_input else "output"
        cost_per_1k = self.cost_per_token[model][cost_type]
        
        return (token_count / 1000) * cost_per_1k
    
    def analyze_laughrx_prompts(self) -> Dict[str, Any]:
        """
        Analyzes token usage for different LaughRx prompt strategies
        """
        # Sample prompts from our previous implementations
        prompts = {
            "system_prompt": """You are LaughRx, the AI Roast Doctor. Your job is to respond to ANY medical symptom or health concern with humor and helpful advice.

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
- Always responsible about serious health concerns""",
            
            "simple_user_prompt": "I have a headache",
            
            "complex_user_prompt": "I have a headache, feel tired all the time, and my back hurts from sitting at my computer all day. I'm a 28-year-old software developer who drinks a lot of coffee and doesn't sleep well.",
            
            "function_calling_prompt": """You are LaughRx with access to specialized functions. Available functions:
- analyze_symptom_severity: Analyzes symptom severity and urgency
- get_lifestyle_recommendations: Provides personalized advice
- check_emergency_symptoms: Detects urgent situations
- calculate_bmi: BMI and health category assessment
- assess_sleep_quality: Sleep pattern analysis

When analyzing symptoms, call appropriate functions and incorporate results into your response.""",
            
            "chain_of_thought_prompt": """You are LaughRx. Show your reasoning step-by-step:

🧠 THINKING PROCESS:
Step 1: Identify and categorize all symptoms mentioned
Step 2: Assess severity and urgency of each symptom
Step 3: Consider possible causes (differential diagnosis)
Step 4: Evaluate risk factors and red flags
Step 5: Determine appropriate treatment/advice level
Step 6: Consider lifestyle factors and modifications
Step 7: Plan follow-up and monitoring needs

Then provide your roast, diagnosis, and advice based on this analysis."""
        }
        
        analysis_results = {}
        
        for prompt_name, prompt_text in prompts.items():
            token_analysis = self.tokenize_text(prompt_text)
            analysis_results[prompt_name] = {
                "token_count": token_analysis.token_count,
                "efficiency_score": token_analysis.efficiency_score,
                "cost_estimate_gpt35": self._estimate_cost(token_analysis.token_count, "gpt-3.5-turbo"),
                "cost_estimate_gpt4": self._estimate_cost(token_analysis.token_count, "gpt-4"),
                "percentage_of_context": {
                    "gpt-3.5-turbo": (token_analysis.token_count / self.model_limits["gpt-3.5-turbo"]["max_tokens"]) * 100,
                    "gpt-4": (token_analysis.token_count / self.model_limits["gpt-4"]["max_tokens"]) * 100
                }
            }
        
        return analysis_results
    
    def optimize_prompt(self, original_prompt: str, target_reduction: float = 0.3) -> Dict[str, Any]:
        """
        Optimizes a prompt to reduce token count while maintaining effectiveness
        """
        original_analysis = self.tokenize_text(original_prompt)
        
        # Apply optimization techniques
        optimized_prompt = self._apply_optimization_techniques(original_prompt)
        optimized_analysis = self.tokenize_text(optimized_prompt)
        
        reduction_achieved = (original_analysis.token_count - optimized_analysis.token_count) / original_analysis.token_count
        
        return {
            "original": {
                "text": original_prompt,
                "tokens": original_analysis.token_count,
                "cost": original_analysis.cost_estimate
            },
            "optimized": {
                "text": optimized_prompt,
                "tokens": optimized_analysis.token_count,
                "cost": optimized_analysis.cost_estimate
            },
            "improvement": {
                "token_reduction": original_analysis.token_count - optimized_analysis.token_count,
                "percentage_reduction": reduction_achieved * 100,
                "cost_savings": original_analysis.cost_estimate - optimized_analysis.cost_estimate,
                "target_met": reduction_achieved >= target_reduction
            }
        }
    
    def _apply_optimization_techniques(self, prompt: str) -> str:
        """
        Applies various optimization techniques to reduce token count
        """
        optimized = prompt
        
        # Remove redundant words
        redundant_phrases = {
            "please ": "",
            "kindly ": "",
            "I would like you to ": "",
            "you should ": "",
            "make sure to ": "",
            "be sure to ": "",
            "it is important to ": "",
            "you need to ": ""
        }
        
        for phrase, replacement in redundant_phrases.items():
            optimized = optimized.replace(phrase, replacement)
        
        # Convert verbose instructions to concise ones
        verbose_to_concise = {
            "provide a detailed analysis": "analyze",
            "give me information about": "explain",
            "tell me about": "describe",
            "I want to know": "explain",
            "can you help me with": "help with",
            "please explain to me": "explain",
            "make sure that you": "ensure you",
            "it is necessary to": "must",
            "in order to": "to",
            "due to the fact that": "because",
            "at this point in time": "now",
            "for the purpose of": "to"
        }
        
        for verbose, concise in verbose_to_concise.items():
            optimized = re.sub(verbose, concise, optimized, flags=re.IGNORECASE)
        
        # Convert sentences to bullet points where appropriate
        if ":" in optimized and len(optimized.split('\n')) > 3:
            lines = optimized.split('\n')
            optimized_lines = []
            for line in lines:
                if line.strip() and not line.strip().startswith('-') and not line.strip().startswith('•'):
                    if any(word in line.lower() for word in ['must', 'should', 'always', 'never', 'include']):
                        optimized_lines.append(f"• {line.strip()}")
                    else:
                        optimized_lines.append(line)
                else:
                    optimized_lines.append(line)
            optimized = '\n'.join(optimized_lines)
        
        # Remove extra whitespace
        optimized = re.sub(r'\s+', ' ', optimized)
        optimized = re.sub(r'\n\s*\n', '\n', optimized)
        
        return optimized.strip()
    
    def calculate_conversation_tokens(self, conversation_history: List[Dict[str, str]], 
                                    model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """
        Calculates total tokens for a conversation including history
        """
        total_tokens = 0
        message_breakdown = []
        
        for i, message in enumerate(conversation_history):
            role = message.get("role", "user")
            content = message.get("content", "")
            
            message_analysis = self.tokenize_text(content)
            total_tokens += message_analysis.token_count
            
            message_breakdown.append({
                "message_number": i + 1,
                "role": role,
                "tokens": message_analysis.token_count,
                "content_preview": content[:50] + "..." if len(content) > 50 else content
            })
        
        model_limits = self.model_limits.get(model, self.model_limits["gpt-3.5-turbo"])
        
        return {
            "total_tokens": total_tokens,
            "message_breakdown": message_breakdown,
            "model_limits": model_limits,
            "usage_percentage": (total_tokens / model_limits["max_tokens"]) * 100,
            "tokens_remaining": model_limits["max_tokens"] - total_tokens,
            "cost_estimate": self._estimate_cost(total_tokens, model, True),
            "recommendations": self._get_conversation_recommendations(total_tokens, model_limits)
        }
    
    def _get_conversation_recommendations(self, total_tokens: int, model_limits: Dict[str, int]) -> List[str]:
        """
        Provides recommendations based on token usage
        """
        recommendations = []
        usage_percentage = (total_tokens / model_limits["max_tokens"]) * 100
        
        if usage_percentage > 90:
            recommendations.append("URGENT: Approaching token limit - summarize conversation history")
        elif usage_percentage > 75:
            recommendations.append("HIGH: Consider removing older messages or summarizing context")
        elif usage_percentage > 50:
            recommendations.append("MEDIUM: Monitor token usage, consider optimization")
        else:
            recommendations.append("LOW: Token usage is healthy")
        
        if total_tokens > model_limits["recommended_prompt"]:
            recommendations.append("Consider using a model with larger context window")
        
        return recommendations
    
    def compare_tokenization_methods(self, text: str) -> Dict[str, TokenAnalysis]:
        """
        Compares different tokenization methods on the same text
        """
        results = {}
        
        for tokenizer_type in TokenizerType:
            analysis = self.tokenize_text(text, tokenizer_type)
            results[tokenizer_type.value] = analysis
        
        return results
    
    def estimate_response_tokens(self, prompt_tokens: int, response_type: str = "standard") -> Dict[str, Any]:
        """
        Estimates response token count based on prompt and response type
        """
        # Typical response patterns for LaughRx
        response_patterns = {
            "roast_only": {"min": 20, "max": 50, "avg": 35},
            "standard": {"min": 80, "max": 150, "avg": 115},  # Roast + Diagnosis + Advice
            "detailed": {"min": 150, "max": 300, "avg": 225},
            "function_calling": {"min": 200, "max": 400, "avg": 300},
            "chain_of_thought": {"min": 300, "max": 600, "avg": 450}
        }
        
        pattern = response_patterns.get(response_type, response_patterns["standard"])
        
        return {
            "estimated_response_tokens": pattern,
            "total_estimated_tokens": prompt_tokens + pattern["avg"],
            "cost_breakdown": {
                "input_cost": self._estimate_cost(prompt_tokens, "gpt-3.5-turbo", True),
                "output_cost": self._estimate_cost(pattern["avg"], "gpt-3.5-turbo", False),
                "total_cost": self._estimate_cost(prompt_tokens, "gpt-3.5-turbo", True) + 
                             self._estimate_cost(pattern["avg"], "gpt-3.5-turbo", False)
            }
        }
    
    def demonstrate_tokenization(self):
        """
        Demonstrates tokenization concepts with LaughRx examples
        """
        print("🎯 LaughRx - Tokens & Tokenization Demo")
        print("=" * 60)
        print("Tokens = How AI models break down and process text!")
        print("=" * 60)
        
        # Show model limits
        print("\n📊 AI MODEL TOKEN LIMITS:")
        print("-" * 50)
        
        for model, limits in self.model_limits.items():
            print(f"\n🤖 {model.upper()}:")
            print(f"   Max Tokens: {limits['max_tokens']:,}")
            print(f"   Recommended Prompt: {limits['recommended_prompt']:,}")
            print(f"   Recommended Response: {limits['recommended_response']:,}")
        
        # Analyze LaughRx prompts
        print(f"\n🔍 LAUGHRX PROMPT ANALYSIS:")
        print("-" * 50)
        
        prompt_analysis = self.analyze_laughrx_prompts()
        
        for prompt_name, analysis in prompt_analysis.items():
            print(f"\n📝 {prompt_name.upper().replace('_', ' ')}:")
            print(f"   Tokens: {analysis['token_count']}")
            print(f"   Efficiency: {analysis['efficiency_score']:.1f} chars/token")
            print(f"   Cost (GPT-3.5): ${analysis['cost_estimate_gpt35']:.4f}")
            print(f"   Context Usage: {analysis['percentage_of_context']['gpt-3.5-turbo']:.1f}%")
        
        # Show tokenization comparison
        print(f"\n🔤 TOKENIZATION METHOD COMPARISON:")
        print("-" * 50)
        
        sample_text = "I have a severe headache and feel nauseous. Please help!"
        tokenization_comparison = self.compare_tokenization_methods(sample_text)
        
        print(f"Sample text: '{sample_text}'")
        for method, analysis in tokenization_comparison.items():
            print(f"\n   {method.upper()}:")
            print(f"   Tokens: {analysis.token_count}")
            print(f"   Efficiency: {analysis.efficiency_score:.1f}")
            print(f"   Sample tokens: {analysis.tokens[:5]}...")
        
        # Show optimization example
        print(f"\n⚡ PROMPT OPTIMIZATION EXAMPLE:")
        print("-" * 50)
        
        verbose_prompt = """Please provide me with a detailed analysis of my symptoms. I would like you to carefully consider all the information I'm giving you and make sure that you provide comprehensive advice. It is important that you analyze everything thoroughly and give me the best possible recommendations for my health concerns."""
        
        optimization_result = self.optimize_prompt(verbose_prompt)
        
        print(f"Original tokens: {optimization_result['original']['tokens']}")
        print(f"Optimized tokens: {optimization_result['optimized']['tokens']}")
        print(f"Reduction: {optimization_result['improvement']['percentage_reduction']:.1f}%")
        print(f"Cost savings: ${optimization_result['improvement']['cost_savings']:.4f}")
        
        print(f"\nOptimized prompt: '{optimization_result['optimized']['text']}'")

def main():
    """
    Main function to demonstrate tokenization concepts
    """
    tokenization_system = LaughRxTokenization()
    tokenization_system.demonstrate_tokenization()
    
    print("\n" + "=" * 60)
    print("🎯 TOKENS & TOKENIZATION - KEY CONCEPTS:")
    print("=" * 60)
    print("✅ Token Limits: Every AI model has maximum input/output limits")
    print("✅ Cost Management: Tokens directly affect API costs")
    print("✅ Prompt Optimization: Reduce tokens while maintaining effectiveness")
    print("✅ Context Management: Handle long conversations efficiently")
    print("✅ Response Planning: Estimate and control output length")
    
    print("\n🔬 TOKENIZATION METHODS:")
    print("• Whitespace: Simple splitting on spaces")
    print("• Word-based: Split on words and punctuation")
    print("• Subword (BPE): Most common in modern AI models")
    print("• Character: Each character is a token")
    
    print("\n💡 OPTIMIZATION STRATEGIES:")
    print("• Remove redundant words and phrases")
    print("• Use bullet points instead of sentences")
    print("• Abbreviate common terms")
    print("• Specify exact response format and length")
    print("• Summarize conversation history when needed")
    
    print("\n🎉 CONGRATULATIONS!")
    print("=" * 60)
    print("🏆 You've completed ALL 9 core AI concepts for LaughRx!")
    print("🚀 Your Generative AI project with Python is ready!")
    print("💻 You now have a complete AI system foundation!")
    
    print("\n📋 WHAT YOU'VE BUILT:")
    print("1. ✅ System & User Prompts - AI personality foundation")
    print("2. ✅ Zero Shot Prompting - Handles any symptom without examples")
    print("3. ✅ Structured Output - Consistent JSON for frontend")
    print("4. ✅ Temperature Control - Smart creativity based on context")
    print("5. ✅ One Shot Prompting - Template-guided responses")
    print("6. ✅ Multi Shot Prompting - Sophisticated, high-quality responses")
    print("7. ✅ Function Calling - Dynamic, data-driven advice")
    print("8. ✅ Chain of Thought - Step-by-step medical reasoning")
    print("9. ✅ Tokens & Tokenization - Understanding AI limits and optimization")
    
    print("\n🔄 NEXT STEPS TO BUILD FULL APP:")
    print("• Choose an AI service (OpenAI, Claude, Gemini)")
    print("• Add API integration to your Python code")
    print("• Build a frontend (React, Vue, or simple HTML)")
    print("• Create a backend API (Flask/FastAPI)")
    print("• Deploy and test your LaughRx application!")

if __name__ == "__main__":
    main()