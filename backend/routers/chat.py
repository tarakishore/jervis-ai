"""
Chat API router for JARVIS.
"""
from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse, HealthResponse
from services.ai_service import ai_service
from services.memory_service import memory_service
from typing import List, Dict

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI response.
    
    - **message**: The user's message
    - **mode**: Chat mode (general, learning, project, productivity)
    - **conversation_id**: Optional ID to continue existing conversation
    """
    # Get or create conversation
    conversation_id = memory_service.get_or_create_conversation(
        request.conversation_id
    )
    
    # Store user message
    memory_service.add_message(
        conversation_id=conversation_id,
        role="user",
        content=request.message,
        mode=request.mode
    )
    
    # Get conversation history for context
    history = memory_service.get_context_messages(conversation_id)
    # Remove the last message (current one) from history
    history = history[:-1] if history else []
    
    # Generate AI response
    response_text = await ai_service.generate_response(
        user_message=request.message,
        mode=request.mode,
        conversation_history=history
    )
    
    # Store assistant response
    memory_service.add_message(
        conversation_id=conversation_id,
        role="assistant",
        content=response_text,
        mode=request.mode
    )
    
    return ChatResponse(
        message=response_text,
        conversation_id=conversation_id,
        mode=request.mode
    )


@router.get("/chat/history/{conversation_id}")
async def get_history(conversation_id: str):
    """Get conversation history for a specific conversation."""
    history = memory_service.get_conversation_history(conversation_id)
    
    if not history:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "mode": msg.mode,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in history.messages
        ]
    }


@router.post("/chat/clear/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear all messages from a conversation."""
    success = memory_service.clear_conversation(conversation_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {"message": "Conversation cleared", "conversation_id": conversation_id}


@router.get("/modes")
async def get_modes() -> List[Dict[str, str]]:
    """Get available chat modes."""
    return ai_service.get_available_modes()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse()
