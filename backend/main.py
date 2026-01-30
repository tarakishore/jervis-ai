"""
JARVIS Backend - FastAPI Application
Personal AI Assistant for Students and Creators
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import chat_router

# Create FastAPI application
app = FastAPI(
    title="JARVIS API",
    description="Personal AI Assistant for Students and Creators",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "JARVIS API",
        "version": "1.0.0",
        "description": "Personal AI Assistant for Students and Creators",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
