import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def get_llm():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to the project .env file "
            "or export it in the shell before running the workflow."
        )

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-5.6-luna",
    )

    return ChatOpenAI(
        model=model_name,
        temperature=0,
    )
