"""
JARVIS Backend Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # AI Provider
    ai_provider: str = "openai"
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
