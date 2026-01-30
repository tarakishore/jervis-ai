"""
Pydantic schemas for JARVIS API.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from uuid import uuid4


# Chat Mode Types
ChatMode = Literal["general", "learning", "project", "productivity"]


class ChatMessage(BaseModel):
    """A single chat message."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    mode: ChatMode = "general"


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=10000)
    mode: ChatMode = "general"
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    message: str
    conversation_id: str
    mode: ChatMode
    timestamp: datetime = Field(default_factory=datetime.now)


class ConversationHistory(BaseModel):
    """Full conversation history."""
    conversation_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)
