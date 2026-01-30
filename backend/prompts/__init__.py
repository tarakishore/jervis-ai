"""Prompts package for JARVIS AI modes."""
from .base import JARVIS_SYSTEM_PROMPT
from .learning import LEARNING_PROMPT
from .project import PROJECT_PROMPT
from .productivity import PRODUCTIVITY_PROMPT

__all__ = [
    "JARVIS_SYSTEM_PROMPT",
    "LEARNING_PROMPT", 
    "PROJECT_PROMPT",
    "PRODUCTIVITY_PROMPT"
]
