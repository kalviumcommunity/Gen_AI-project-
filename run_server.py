"""
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
