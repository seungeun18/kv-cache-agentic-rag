"""Fail fast when the project is not running from its own virtual environment."""

from importlib.util import find_spec
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VENV = (PROJECT_ROOT / ".venv").resolve()
REQUIRED_MODULES = (
    "faiss",
    "langchain_community",
    "langchain_huggingface",
    "langchain_openai",
    "langgraph",
    "sentence_transformers",
)


def main() -> None:
    executable = Path(sys.executable).absolute()
    prefix = Path(sys.prefix).resolve()

    print(f"sys.executable: {executable}")
    print(f"sys.prefix:     {prefix}")

    if prefix != EXPECTED_VENV:
        raise SystemExit(
            "ERROR: this project is not using its .venv. Run "
            "`source .venv/bin/activate` and try again."
        )

    missing = [name for name in REQUIRED_MODULES if find_spec(name) is None]
    if missing:
        raise SystemExit(
            "ERROR: missing packages in .venv: " + ", ".join(missing)
        )

    foreign_paths = [
        entry
        for entry in sys.path
        if entry.startswith("/opt/homebrew/lib/python")
    ]
    if foreign_paths:
        raise SystemExit(
            "ERROR: global Homebrew site-packages leaked into .venv: "
            + ", ".join(foreign_paths)
        )

    print("Environment OK: all required modules resolve inside the project .venv.")


if __name__ == "__main__":
    main()
