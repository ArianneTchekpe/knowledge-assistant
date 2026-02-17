"""
Obsidian Knowledge Assistant
Système RAG pour interroger vos notes Obsidian
"""

from .config import Config
from .knowledge_assistant import KnowledgeAssistant

__version__ = "1.0.0"

__all__ = [
    "Config",
    "KnowledgeAssistant"
]
