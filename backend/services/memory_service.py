"""
Memory service for managing conversation history.
"""
from typing import Dict, List, Optional
from datetime import datetime
from uuid import uuid4
from models.schemas import ChatMessage, ConversationHistory


class MemoryService:
    """
    In-memory conversation storage.
    In production, this would use a database like Redis or PostgreSQL.
    """
    
    def __init__(self):
        self._conversations: Dict[str, ConversationHistory] = {}
        self._max_messages: int = 20  # Keep last N messages for context
    
    def create_conversation(self) -> str:
        """Create a new conversation and return its ID."""
        conversation_id = str(uuid4())
        now = datetime.now()
        
        self._conversations[conversation_id] = ConversationHistory(
            conversation_id=conversation_id,
            messages=[],
            created_at=now,
            updated_at=now
        )
        
        return conversation_id
    
    def get_or_create_conversation(self, conversation_id: Optional[str]) -> str:
        """Get existing conversation or create new one."""
        if conversation_id and conversation_id in self._conversations:
            return conversation_id
        return self.create_conversation()
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        mode: str = "general"
    ) -> ChatMessage:
        """Add a message to the conversation."""
        if conversation_id not in self._conversations:
            self.create_conversation()
            self._conversations[conversation_id] = ConversationHistory(
                conversation_id=conversation_id,
                messages=[],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        
        message = ChatMessage(
            role=role,
            content=content,
            mode=mode
        )
        
        conversation = self._conversations[conversation_id]
        conversation.messages.append(message)
        conversation.updated_at = datetime.now()
        
        # Trim old messages to prevent context overflow
        if len(conversation.messages) > self._max_messages:
            conversation.messages = conversation.messages[-self._max_messages:]
        
        return message
    
    def get_messages(self, conversation_id: str) -> List[ChatMessage]:
        """Get all messages for a conversation."""
        if conversation_id not in self._conversations:
            return []
        return self._conversations[conversation_id].messages
    
    def get_context_messages(self, conversation_id: str) -> List[Dict[str, str]]:
        """Get messages formatted for OpenAI API."""
        messages = self.get_messages(conversation_id)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
            if msg.role in ["user", "assistant"]
        ]
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear all messages from a conversation."""
        if conversation_id in self._conversations:
            self._conversations[conversation_id].messages = []
            self._conversations[conversation_id].updated_at = datetime.now()
            return True
        return False
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation entirely."""
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False
    
    def get_conversation_history(
        self, 
        conversation_id: str
    ) -> Optional[ConversationHistory]:
        """Get full conversation history."""
        return self._conversations.get(conversation_id)


# Global memory service instance
memory_service = MemoryService()
