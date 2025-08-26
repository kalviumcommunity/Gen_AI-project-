"""
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
                    "cost": "free tier",
                    "top_p": getattr(ai_client, "top_p", None)
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
