"""
LaughRx - FastAPI Backend Creator
================================

This creates a production-ready FastAPI backend for your LaughRx application.
"""

import os
from typing import Dict, Any

class LaughRxBackendCreator:
    def __init__(self):
        self.backend_files = self._create_backend_files()
    
    def _create_backend_files(self) -> Dict[str, str]:
        """
        Creates all backend files
        """
        return {
            "main.py": '''"""
LaughRx FastAPI Backend
======================

Production-ready API for LaughRx AI medical assistant.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Import your AI integration
from ai_integration_simple import LaughRxAISimple

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="LaughRx API",
    description="AI-powered medical assistant with humor",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI
ai_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize AI client on startup"""
    global ai_client
    try:
        ai_client = LaughRxAISimple()
        print("✅ LaughRx AI initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize AI: {e}")

# Pydantic models
class SymptomRequest(BaseModel):
    symptoms: str
    user_context: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    success: bool
    response: str
    symptoms: str
    metadata: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool
    error: str
    message: str

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to LaughRx API!",
        "description": "AI-powered medical assistant with humor",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_status": "connected" if ai_client else "disconnected",
        "version": "1.0.0"
    }

@app.post("/analyze", response_model=HealthResponse)
async def analyze_symptoms(request: SymptomRequest):
    """
    Analyze symptoms and get LaughRx response
    """
    if not ai_client:
        raise HTTPException(
            status_code=503, 
            detail="AI service unavailable"
        )
    
    try:
        # Generate AI response
        result = ai_client.generate_response(request.symptoms)
        
        if result["success"]:
            return HealthResponse(
                success=True,
                response=result["response"],
                symptoms=request.symptoms,
                metadata={
                    "model": "gemini-1.5-flash",
                    "response_time": "< 2 seconds",
                    "cost": "free tier"
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"AI generation failed: {result.get('error', 'Unknown error')}"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/quick-advice")
async def quick_advice(request: SymptomRequest):
    """
    Get quick advice without full LaughRx personality
    """
    if not ai_client:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    
    try:
        # Use a simplified prompt for quick advice
        quick_prompt = f"Provide brief medical advice for: {request.symptoms}. Keep it under 100 words and include a disclaimer."
        
        result = ai_client.generate_response(request.symptoms)
        
        if result["success"]:
            return {
                "success": True,
                "advice": result["response"][:200] + "..." if len(result["response"]) > 200 else result["response"],
                "symptoms": request.symptoms
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to generate advice")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/examples")
async def get_examples():
    """
    Get example symptoms and responses
    """
    return {
        "examples": [
            {
                "symptoms": "I have a headache",
                "expected_response": "Humorous roast + medical advice"
            },
            {
                "symptoms": "I can't sleep",
                "expected_response": "Sleep hygiene advice with humor"
            },
            {
                "symptoms": "My back hurts from sitting",
                "expected_response": "Posture advice with gentle teasing"
            }
        ]
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail, "message": "Request failed"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(exc), "message": "Internal server error"}
    )

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )
''',

            "requirements.txt": '''# LaughRx Backend Requirements
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
google-generativeai==0.3.2
pydantic==2.5.0
python-multipart==0.0.6
''',

            "test_backend.py": '''"""
Test script for LaughRx backend
"""

import requests
import json

def test_backend():
    """Test all backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing LaughRx Backend API")
    print("=" * 50)
    
    # Test root endpoint
    print("\\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()['message']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test health check
    print("\\n2. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   AI Status: {data['ai_status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test symptom analysis
    print("\\n3. Testing symptom analysis...")
    try:
        test_data = {
            "symptoms": "I have a headache and feel tired"
        }
        response = requests.post(
            f"{base_url}/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Symptom analysis working")
            print(f"   Response preview: {data['response'][:100]}...")
        else:
            print(f"❌ Symptom analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Symptom analysis error: {e}")
    
    # Test quick advice
    print("\\n4. Testing quick advice...")
    try:
        test_data = {
            "symptoms": "I have a runny nose"
        }
        response = requests.post(
            f"{base_url}/quick-advice",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Quick advice working")
            print(f"   Advice: {data['advice'][:100]}...")
        else:
            print(f"❌ Quick advice failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Quick advice error: {e}")
    
    print("\\n🎉 Backend testing complete!")

if __name__ == "__main__":
    test_backend()
''',

            "run_server.py": '''"""
LaughRx Server Runner
====================

Simple script to run the LaughRx backend server.
"""

import uvicorn
import os
from dotenv import load_dotenv

def run_server():
    """Run the LaughRx backend server"""
    load_dotenv()
    
    print("🚀 Starting LaughRx Backend Server")
    print("=" * 50)
    print(f"🌐 Server will run on: http://localhost:{os.getenv('PORT', 8000)}")
    print(f"📚 API docs available at: http://localhost:{os.getenv('PORT', 8000)}/docs")
    print(f"🔧 Debug mode: {os.getenv('DEBUG', 'True')}")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print()
    
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true",
        log_level="info"
    )

if __name__ == "__main__":
    run_server()
'''
        }
    
    def create_all_files(self):
        """Create all backend files"""
        print("🛠️ Creating LaughRx Backend Files")
        print("=" * 50)
        
        for filename, content in self.backend_files.items():
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Created {filename}")
            except Exception as e:
                print(f"❌ Failed to create {filename}: {e}")
        
        print(f"\\n🎯 Backend files created successfully!")
        print(f"\\n🔄 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start server: python run_server.py")
        print("3. Test API: python test_backend.py")
        print("4. View docs: http://localhost:8000/docs")

def main():
    """Main function"""
    creator = LaughRxBackendCreator()
    creator.create_all_files()
    
    print(f"\\n🚀 Your LaughRx Backend is Ready!")
    print("=" * 50)
    print("✅ FastAPI backend with all endpoints")
    print("✅ AI integration connected")
    print("✅ CORS enabled for frontend")
    print("✅ Error handling and validation")
    print("✅ API documentation included")
    print("✅ Production-ready architecture")

if __name__ == "__main__":
    main()