import json
from pathlib import Path
from typing import List, Dict, Any


# Base directory: app/
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "mock_transactions.json"


def load_mock_transactions() -> List[Dict[str, Any]]:
    """
    Load mock transactions from the JSON file.
    """
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data["transactions"]


def summarize_spending(transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Summarise negative (spending) amounts by category.
    Income (positive amounts) is ignored.
    """
    totals: Dict[str, float] = {}

    for tx in transactions:
        amt = tx["amount"]
        category = tx["category"]

        # ignore income
        if amt > 0:
            continue

        totals.setdefault(category, 0.0)
        totals[category] += abs(amt)

    return totals
