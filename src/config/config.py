"""
Centralized Configuration Module
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Project Configuration"""
    # API Keys & Model Defaults
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
    
    # UI Configuration
    PAGE_TITLE = "DocuRAG"
    PAGE_ICON = "🔮"
    
    # Asset Paths
    CSS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
