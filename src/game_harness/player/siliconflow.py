"""Build a LangChain chat model for the SiliconFlow player."""

import math
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel


def create_player(
    *,
    api_key: str | None = None,
    model: str = "moonshotai/Kimi-K2.7-Code",
    timeout: float = 600,
) -> BaseChatModel:
    """Create a model supporting invoke(messages) and bind_tools(tools).

    Load .env from the working directory without overriding environment variables.
    Tool execution and conversation history belong to the caller.
    """
    load_dotenv(".env", override=False)
    key = api_key if api_key is not None else os.environ.get("SILICONFLOW_API_KEY", "")
    if not key.strip():
        raise ValueError("Set SILICONFLOW_API_KEY or pass api_key")
    if not model.strip():
        raise ValueError("model must not be empty")
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be a finite positive number")

    return init_chat_model(
        model=model,
        model_provider="openai",
        api_key=key,
        base_url="https://api.siliconflow.cn/v1",
        timeout=timeout,
        max_retries=0,
        use_responses_api=False,
        extra_body={"enable_thinking": False},
    )
