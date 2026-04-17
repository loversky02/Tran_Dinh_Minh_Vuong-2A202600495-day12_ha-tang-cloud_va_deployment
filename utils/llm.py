"""
LLM Module - OpenAI with Mock Fallback
Automatically uses OpenAI if API key available, otherwise falls back to mock.
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not installed. Using mock LLM.")

# Import mock as fallback
from utils.mock_llm import ask as mock_ask

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))

# Initialize OpenAI client if available
openai_client: Optional[OpenAI] = None
if OPENAI_AVAILABLE and OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info(f"OpenAI initialized with model: {LLM_MODEL}")
    except Exception as e:
        logger.warning(f"Failed to initialize OpenAI: {e}. Using mock LLM.")
        openai_client = None


def ask(question: str, system_prompt: Optional[str] = None) -> str:
    """
    Ask LLM a question.
    Uses OpenAI if available, otherwise falls back to mock.
    
    Args:
        question: User's question
        system_prompt: Optional system prompt (default: helpful assistant)
    
    Returns:
        LLM response as string
    """
    # Use OpenAI if available
    if openai_client:
        try:
            return _ask_openai(question, system_prompt)
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}. Falling back to mock.")
            return mock_ask(question)
    
    # Fallback to mock
    logger.debug("Using mock LLM (no OpenAI API key)")
    return mock_ask(question)


def _ask_openai(question: str, system_prompt: Optional[str] = None) -> str:
    """
    Call OpenAI API.
    
    Args:
        question: User's question
        system_prompt: Optional system prompt
    
    Returns:
        OpenAI response
    
    Raises:
        Exception: If API call fails
    """
    if not system_prompt:
        system_prompt = "You are a helpful AI assistant deployed on Railway cloud platform."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    response = openai_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=0.7,
    )
    
    answer = response.choices[0].message.content
    
    # Log token usage
    usage = response.usage
    logger.info(f"OpenAI tokens: input={usage.prompt_tokens}, output={usage.completion_tokens}, total={usage.total_tokens}")
    
    return answer


def get_llm_info() -> dict:
    """
    Get information about current LLM configuration.
    
    Returns:
        Dict with LLM type, model, and status
    """
    if openai_client:
        return {
            "type": "openai",
            "model": LLM_MODEL,
            "max_tokens": MAX_TOKENS,
            "status": "active"
        }
    else:
        return {
            "type": "mock",
            "model": "mock-llm",
            "max_tokens": "N/A",
            "status": "active",
            "note": "Set OPENAI_API_KEY to use real OpenAI"
        }
