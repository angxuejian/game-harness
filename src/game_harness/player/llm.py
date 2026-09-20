"""Build a LangChain chat model for the SiliconFlow player."""

import math
import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel


def create_player(
    *,
    api_key: str | None = None,
    model: str = "deepseek-ai/DeepSeek-V4-Flash",
    timeout: float = 100,
) -> BaseChatModel:
    """Create a model supporting invoke(messages) and bind_tools(tools).

    Load .env from the working directory without overriding environment variables.
    Tool execution and conversation history belong to the caller.
    """
    load_dotenv(".env", override=False)
    key = api_key if api_key is not None else os.environ.get("API_KEY", "")
    if not key.strip():
        raise ValueError("Set API_KEY or pass api_key")
    if not model.strip():
        raise ValueError("model must not be empty")
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be a finite positive number")

    base_url = os.environ.get("BASE_URL", "")
    extra_body = json.loads(os.environ.get("EXTRA_BODY", "{}"))

    return init_chat_model(
        model=model,
        model_provider="openai",
        api_key=key,
        base_url=base_url,
        timeout=timeout,
        max_retries=0,
        use_responses_api=False,
        extra_body=extra_body,
    )
