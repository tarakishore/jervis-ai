"""
AI Service for OpenAI integration.
"""
from typing import List, Dict, Optional
from openai import OpenAI
from config import settings
from prompts import (
    JARVIS_SYSTEM_PROMPT,
    LEARNING_PROMPT,
    PROJECT_PROMPT,
    PRODUCTIVITY_PROMPT
)



class MockAIService:
    """
    Mock AI service for demo purposes when no API key is available.
    """
    async def generate_response(self, user_message: str, mode: str, conversation_history: list) -> str:
        import asyncio
        await asyncio.sleep(1.5)  # Simulate network delay
        
        if mode == "learning":
            return (
                "## 🎓 Learning Mode (Demo)\n\n"
                "This is a simulated response because **no OpenAI API key** was detected.\n\n"
                "### In a real session, I would:\n"
                "1. Explain the concept of **" + user_message[:20] + "...** in detail\n"
                "2. Create a custom study plan for you\n"
                "3. Generate practice questions\n\n"
                "### Try adding a key later!\n"
                "You can get one at [platform.openai.com](https://platform.openai.com/api-keys)"
            )
            
        elif mode == "project":
            return (
                "## 🛠️ Project Builder (Demo)\n\n"
                "This is a simulated response because **no OpenAI API key** was detected.\n\n"
                "### In a real session, I would:\n"
                "- helping you build a project about: **" + user_message[:20] + "...**\n"
                "- Suggest a full tech stack (e.g., React, FastAPI)\n"
                "- Write the actual code for you\n\n"
                "To see me really work, please add an API key in `backend/.env`!"
            )
            
        elif mode == "productivity":
            return (
                "## 📋 Productivity Mode (Demo)\n\n"
                "This is a simulated response because **no OpenAI API key** was detected.\n\n"
                "### I can help you with:\n"
                "- Prioritizing your task: **" + user_message[:20] + "...**\n"
                "- Creating a daily schedule\n"
                "- Setting SMART goals\n\n"
                "*Add an OpenAI API key to unlock full potential!*"
            )
            
        else:  # General
            return (
                "## 🤖 JARVIS (Demo Mode)\n\n"
                "I'm running in **Demo Mode** right now because I didn't find a valid OpenAI API key.\n\n"
                "I can show you the interface, but I can't generate real intelligence yet!\n\n"
                "### How to get a real Key:\n"
                "1. Go to [platform.openai.com](https://platform.openai.com/signup)\n"
                "2. Sign up/Log in\n"
                "3. Click **'Create new secret key'**\n"
                "4. Paste it into your `backend/.env` file"
            )


class AIService:
    """
    Service for interacting with OpenAI API.
    Handles prompt construction and response generation.
    """
    
    def __init__(self):
        self.provider = settings.ai_provider.lower()
        self.api_key = settings.openai_api_key
        
        # Determine if we need to use Mock Service
        # Mock is used if:
        # 1. Provider is openai AND key is missing/default
        # 2. Provider is unknown
        
        if self.provider == "ollama":
            # For Ollama, we use the OpenAI client but point it to local URL
            print(f"Using Local AI (Ollama) with model: {settings.ollama_model}")
            self.client = OpenAI(
                base_url=settings.ollama_base_url,
                api_key="ollama"  # Required but ignored by Ollama
            )
            self.model = settings.ollama_model
            self.is_mock = False
            
        elif self.provider == "openai":
            # Check if key is real or default/empty
            self.is_mock = not self.api_key or self.api_key == "your-openai-api-key-here" or self.api_key == ""
            
            if not self.is_mock:
                self.client = OpenAI(api_key=self.api_key)
                self.model = settings.openai_model
            else:
                print("⚠️ WARNING: No valid OpenAI API Key found. Using Mock Service.")
                self.mock_service = MockAIService()
                
        else:
            print(f"⚠️ Unknown provider '{self.provider}'. Falling back to Mock.")
            self.is_mock = True
            self.mock_service = MockAIService()
        
        # Mode-specific prompts
        self.mode_prompts = {
            "general": "",
            "learning": LEARNING_PROMPT,
            "project": PROJECT_PROMPT,
            "productivity": PRODUCTIVITY_PROMPT
        }
    
    def _build_system_prompt(self, mode: str) -> str:
        """Build the complete system prompt based on mode."""
        base_prompt = JARVIS_SYSTEM_PROMPT
        mode_prompt = self.mode_prompts.get(mode, "")
        
        if mode_prompt:
            return f"{base_prompt}\n\n---\n\n{mode_prompt}"
        return base_prompt
    
    async def generate_response(
        self,
        user_message: str,
        mode: str = "general",
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate an AI response for the user's message.
        """
        # Fallback to mock if no key
        if self.is_mock:
            return await self.mock_service.generate_response(user_message, mode, conversation_history)

        # Build messages array for API
        messages = [
            {"role": "system", "content": self._build_system_prompt(mode)}
        ]
        
        # Add conversation history for context
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Log error in production
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            
            # Provide helpful fallback for common issues
            if "api_key" in str(e).lower():
                self.is_mock = True # Switch to mock for future requests if key is invalid
                error_message = (
                    "⚠️ **Authentication Failed**\n\n"
                    "The provided API key seems invalid. I've switched to **Demo Mode** for now.\n"
                    "Please check your key in `backend/.env`."
                )
            elif "rate_limit" in str(e).lower():
                error_message = (
                    "⚠️ **Rate Limit**\n\n"
                    "The API rate limit has been reached. Please wait a moment and try again."
                )
            
            return error_message
    
    def get_available_modes(self) -> List[Dict[str, str]]:
        """Get list of available chat modes with descriptions."""
        return [
            {
                "id": "general",
                "name": "General Chat",
                "description": "Natural conversation with JARVIS",
                "icon": "💬"
            },
            {
                "id": "learning",
                "name": "Learning Mode",
                "description": "Study help, explanations, and practice",
                "icon": "📚"
            },
            {
                "id": "project",
                "name": "Project Builder",
                "description": "Build projects from ideas to code",
                "icon": "🛠️"
            },
            {
                "id": "productivity",
                "name": "Productivity",
                "description": "Task management and planning",
                "icon": "📋"
            }
        ]


# Global AI service instance
ai_service = AIService()
