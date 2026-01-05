import json


def parse_ai_json(ai_text: str) -> dict:
    """
    Clean up AI output and parse it as JSON.
    Handles cases where the model wraps JSON in ```json ... ``` fences.
    """
    cleaned = ai_text.strip()

    # If the model wrapped the JSON in a markdown code block
    if cleaned.startswith("```"):
        # Remove leading and trailing backticks
        cleaned = cleaned.strip("`").lstrip()

        # After this we might have something like: "json\n{ ... }"
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]  # remove 'json'
        cleaned = cleaned.strip()

    # Now cleaned should be pure JSON text
    return json.loads(cleaned)
