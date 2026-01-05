import json
from pathlib import Path
from typing import List, Dict, Any


BASE_DIR = Path(__file__).resolve().parent.parent
KB_PATH = BASE_DIR / "data" / "knowledge_base.json"

_KB_CACHE: List[Dict[str, Any]] | None = None


def load_knowledge_base() -> List[Dict[str, Any]]:
    """
    Load the knowledge base from JSON (cached after first read).
    """
    global _KB_CACHE
    if _KB_CACHE is None:
        with open(KB_PATH, "r", encoding="utf-8") as f:
            _KB_CACHE = json.load(f)
    return _KB_CACHE


def get_relevant_chunks(dominant_category: str) -> List[Dict[str, Any]]:
    """
    Return knowledge chunks that are relevant to a given dominant category.
    Includes:
      - entries with matching 'category'
      - multi-category entries where the category appears in 'categories'
    """
    kb = load_knowledge_base()
    relevant: List[Dict[str, Any]] = []

    for item in kb:
        cat = item.get("category")
        cats = item.get("categories")

        if cat == dominant_category:
            relevant.append(item)
        elif isinstance(cats, list) and dominant_category in cats:
            relevant.append(item)

    return relevant


def build_guidance_text(dominant_category: str, user_name: str = "friend") -> str:
    """
    Build a plain-text guidance block from the knowledge base for the model to use.
    Replaces {user_name} placeholders and includes questions/options where present.
    """
    chunks = get_relevant_chunks(dominant_category)
    if not chunks:
        return ""

    parts: List[str] = []

    for item in chunks:
        # main text with user_name injected
        text = item.get("text", "").replace("{user_name}", user_name)
        if text:
            parts.append(text)

        # if it's a check-in style entry, append question + options
        if item.get("type") == "multi_category_checkin":
            question = item.get("question")
            options = item.get("options", [])
            if question and options:
                option_lines = "\n".join(f"- {opt}" for opt in options)
                parts.append(f"{question}\n{option_lines}")

    return "\n\n".join(parts)


def get_checkin_for_category(dominant_category: str) -> dict | None:
    """
    Return a single 'check-in' style entry (with question + options)
    for a given dominant category, if available.
    """
    chunks = get_relevant_chunks(dominant_category)
    for item in chunks:
        if item.get("type") == "multi_category_checkin":
            return item
    return None
