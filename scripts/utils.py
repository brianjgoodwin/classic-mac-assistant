"""Shared utilities for the vintage Apple tracker script."""

import os
import datetime

import anthropic


MODEL = "claude-sonnet-4-6"


def get_client() -> anthropic.Anthropic:
    """Return an Anthropic client, or exit with a clear message if the key is missing."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        raise SystemExit(1)
    return anthropic.Anthropic(api_key=api_key)


def call_with_search(
    client: anthropic.Anthropic,
    system: str,
    user_message: str,
    max_continuations: int = 3,
) -> str:
    """Make an API call with web search tool, handling pause_turn continuations."""
    messages = [{"role": "user", "content": user_message}]
    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 15}]

    response = None
    for _ in range(max_continuations + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=system,
            tools=tools,
            messages=messages,
        )
        if response.stop_reason != "pause_turn":
            break
        # Continue the conversation with the assistant's partial response
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": "Continue."})

    if response is None:
        raise RuntimeError("API call failed to produce a response")

    text = _extract_text(response)
    if not text or not text.strip():
        raise RuntimeError("API response contained no text content")

    return text


def _extract_text(response) -> str:
    """Extract all text blocks from an API response."""
    return "\n".join(b.text for b in response.content if b.type == "text")


# --- File helpers ---


def read_file(path: str) -> str | None:
    """Read a file and return its contents, or None if it doesn't exist."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except (IOError, OSError) as e:
        print(f"Warning: Could not read {path}: {e}")
        return None


def write_file(path: str, content: str) -> None:
    """Write content to a file, creating parent directories if needed."""
    try:
        dir_path = os.path.dirname(path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except (IOError, OSError) as e:
        raise RuntimeError(f"Failed to write to {path}: {e}") from e


# --- Date helpers ---


def today() -> str:
    """Return today's date as YYYY-MM-DD."""
    return datetime.date.today().isoformat()


def week_id() -> str:
    """Return the current ISO week as YYYY-WNN."""
    d = datetime.date.today()
    iso = d.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"
