import json
from typing import Dict, List

from config import DATASET_PATH

def load_dataset(path: str = DATASET_PATH) -> Dict:
    """Load the full dataset JSON and return its content as a dictionary."""
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def load_tickets(data: Dict) -> List[Dict]:
    """Load and validate support tickets."""
    try:
        tickets = data.get('tickets', [])
        return tickets
    except Exception as e:
        raise RuntimeError(f"Failed to load tickets: {str(e)}")

def prepare_corpus(tickets: List[Dict]) -> List[str]:
    """Prepare the searchable text corpus including resolutions."""
    texts = []
    for t in tickets:
        text = (f"Title: {t['title']}. "
                f"Issue: {t['issue']}. "
                f"Resolution: {t['resolution']} "
                f"(Browser: {t['browser']}, OS: {t['os']}, Customer: {t['customer_type']})")
        texts.append(text)
    return texts