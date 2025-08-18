"""
LaughRx System Tester
====================

This script tests all 9 AI concepts to ensure everything is working properly.
Run this after installing Python to verify your LaughRx system!
"""

import sys
import os
import importlib.util

def test_file_exists(file_path, concept_name):
    """Test if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {concept_name}: File exists")
        return True
    else:
        print(f"❌ {concept_name}: File missing")
        return False

def test_file_imports(file_path, concept_name):
    """Test if a file can be imported without errors"""
    try:
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ {concept_name}: Imports successfully")
        return True
    except Exception as e:
        print(f"❌ {concept_name}: Import error - {str(e)[:50]}...")
        return False

def test_class_functionality(file_path, class_name, concept_name):
    """Test if main class can be instantiated"""
    try:
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get the class and instantiate it
        cls = getattr(module, class_name)
        instance = cls()
        print(f"✅ {concept_name}: Class instantiated successfully")
        return True, instance
    except Exception as e:
        print(f"❌ {concept_name}: Class error - {str(e)[:50]}...")
        return False, None

def run_comprehensive_test():
    """Run comprehensive test of all LaughRx components"""
    print("🎯 LaughRx System Comprehensive Test")
    print("=" * 60)
    print("Testing all 9 AI concepts...")
    print("=" * 60)
    
    # Define all components
    components = [
        {
            "file": "system_user_prompts.py",
            "class": "LaughRxPrompts",
            "name": "System & User Prompts"
        },
        {
            "file": "zero_shot_prompting.py",
            "class": "LaughRxZeroShotPrompting",
            "name": "Zero Shot Prompting"
        },
        {
            "file": "structured_output.py",
            "class": "LaughRxStructuredOutput",
            "name": "Structured Output"
        },
        {
            "file": "temperature_control.py",
            "class": "LaughRxTemperatureControl",
            "name": "Temperature Control"
        },
        {
            "file": "one_shot_prompting.py",
            "class": "LaughRxOneShotPrompting",
            "name": "One Shot Prompting"
        },
        {
            "file": "multi_shot_prompting.py",
            "class": "LaughRxMultiShotPrompting",
            "name": "Multi Shot Prompting"
        },
        {
            "file": "function_calling.py",
            "class": "LaughRxFunctionCalling",
            "name": "Function Calling"
        },
        {
            "file": "chain_of_thought.py",
            "class": "LaughRxChainOfThought",
            "name": "Chain of Thought"
        },
        {
            "file": "tokens_and_tokenization.py",
            "class": "LaughRxTokenization",
            "name": "Tokens & Tokenization"
        }
    ]
    
    base_path = r"c:\Users\Palchhi Jain\Desktop\Gen_AI-project-"
    
    results = {
        "total_components": len(components),
        "files_exist": 0,
        "imports_work": 0,
        "classes_work": 0,
        "working_instances": []
    }
    
    print(f"\n📁 TESTING FILE EXISTENCE:")
    print("-" * 40)
    
    for component in components:
        file_path = os.path.join(base_path, component["file"])
        if test_file_exists(file_path, component["name"]):
            results["files_exist"] += 1
    
    print(f"\n📦 TESTING IMPORTS:")
    print("-" * 40)
    
    for component in components:
        file_path = os.path.join(base_path, component["file"])
        if os.path.exists(file_path):
            if test_file_imports(file_path, component["name"]):
                results["imports_work"] += 1
    
    print(f"\n🏗️ TESTING CLASS INSTANTIATION:")
    print("-" * 40)
    
    for component in components:
        file_path = os.path.join(base_path, component["file"])
        if os.path.exists(file_path):
            success, instance = test_class_functionality(file_path, component["class"], component["name"])
            if success:
                results["classes_work"] += 1
                results["working_instances"].append({
                    "name": component["name"],
                    "class": component["class"],
                    "instance": instance
                })
    
    # Print summary
    print(f"\n📊 TEST RESULTS SUMMARY:")
    print("=" * 60)
    print(f"Files Exist: {results['files_exist']}/{results['total_components']}")
    print(f"Imports Work: {results['imports_work']}/{results['total_components']}")
    print(f"Classes Work: {results['classes_work']}/{results['total_components']}")
    
    success_rate = (results['classes_work'] / results['total_components']) * 100
    print(f"Overall Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n🎉 PERFECT! All components working!")
        print(f"✅ Your LaughRx system is fully functional!")
    elif success_rate >= 80:
        print(f"\n🎯 EXCELLENT! Most components working!")
        print(f"✅ Your LaughRx system is mostly functional!")
    elif success_rate >= 60:
        print(f"\n⚠️ GOOD! Some issues to fix.")
    else:
        print(f"\n❌ NEEDS WORK! Several components have issues.")
    
    return results

def test_sample_functionality():
    """Test sample functionality from working components"""
    print(f"\n🧪 TESTING SAMPLE FUNCTIONALITY:")
    print("-" * 50)
    
    try:
        # Test System Prompts
        sys.path.append(r"c:\Users\Palchhi Jain\Desktop\Gen_AI-project-")
        from system_user_prompts import LaughRxPrompts
        
        prompt_system = LaughRxPrompts()
        sample_prompt = prompt_system.create_user_prompt("I have a headache")
        print(f"✅ System Prompts: Generated prompt ({len(sample_prompt)} chars)")
        
        # Test Tokenization
        from tokens_and_tokenization import LaughRxTokenization
        
        token_system = LaughRxTokenization()
        token_analysis = token_system.tokenize_text("I have a headache")
        print(f"✅ Tokenization: Analyzed text ({token_analysis.token_count} tokens)")
        
        # Test Structured Output
        from structured_output import LaughRxStructuredOutput
        
        output_system = LaughRxStructuredOutput()
        structured_response = output_system.create_structured_response(
            "I have a headache", "mild", "lifestyle"
        )
        print(f"✅ Structured Output: Generated JSON response")
        
        print(f"\n🎯 SAMPLE FUNCTIONALITY TEST: PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Sample functionality error: {str(e)[:100]}...")
        return False

def main():
    """Main test function"""
    print("🚀 Starting LaughRx System Test...")
    print("This will verify all your AI concepts are working!\n")
    
    # Run comprehensive test
    results = run_comprehensive_test()
    
    # Test sample functionality if components are working
    if results["classes_work"] >= 3:
        test_sample_functionality()
    
    print(f"\n🔄 NEXT STEPS:")
    print("-" * 30)
    
    if results["classes_work"] == results["total_components"]:
        print("✅ All systems working! Ready to:")
        print("   1. Choose an AI service (OpenAI, Claude, Gemini)")
        print("   2. Add API integration")
        print("   3. Build frontend interface")
        print("   4. Deploy your LaughRx app!")
    else:
        print("⚠️ Fix any issues above, then:")
        print("   1. Re-run this test")
        print("   2. Proceed with AI integration")
    
    print(f"\n🎉 Test Complete!")

if __name__ == "__main__":
    main()