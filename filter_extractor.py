import re
from typing import Dict, List, Optional
from fuzzywuzzy import fuzz
from config import BROWSER_MAP, BROWSER_SYNONYMS, OS_SYNONYMS, CUSTOMER_SYNONYMS, STAGE_SYNONYMS

USE_FUZZY_MATCHING = False
FUZZ_THRESHOLD = 80

def fuzzy_match(text: str, choices: List[str], threshold: int = FUZZ_THRESHOLD) -> Optional[str]:
    """Perform fuzzy matching on text against a list of choices."""
    best_match = None
    best_score = threshold
    for choice in choices:
        score = fuzz.partial_ratio(text, choice)
        if score > best_score:
            best_score = score
            best_match = choice
    return best_match

def extract_filters(query: str) -> Dict[str, str]:
    """Extract metadata filters from a natural language query."""
    q = query.strip().lower()
    filters: Dict[str, str] = {}

    # Stage detection
    if 'oauth' in q:
        filters['stage'] = 'consent'
    else:
        if USE_FUZZY_MATCHING:
            for canon, syns in STAGE_SYNONYMS.items():
                matched_syn = fuzzy_match(q, syns)
                if matched_syn:
                    filters['stage'] = canon
                    break
        else:
            for canon, syns in STAGE_SYNONYMS.items():
                if any(s in q for s in syns):
                    filters['stage'] = canon
                    break

    # Browser detection
    for pat, name, version_group in BROWSER_MAP:
        m = re.search(pat, q)
        if m:
            filters['browser'] = name
            if version_group and m.group(version_group):
                filters['browser_version'] = m.group(version_group)
            break
    else:
        if USE_FUZZY_MATCHING:
            for canon, syns in BROWSER_SYNONYMS.items():
                matched_syn = fuzzy_match(q, syns)
                if matched_syn:
                    filters['browser'] = canon
                    break

    # OS detection
    for specific in ["macos monterey", "macos sonoma", "macos ventura", "linux mint", "linux ubuntu"]:
        if USE_FUZZY_MATCHING:
            matched_syn = fuzzy_match(q, OS_SYNONYMS[specific])
            if matched_syn:
                filters['os'] = specific
                break
        else:
            if any(s in q for s in OS_SYNONYMS[specific]):
                filters['os'] = specific
                break
    else:
        for canon, syns in OS_SYNONYMS.items():
            if USE_FUZZY_MATCHING:
                matched_syn = fuzzy_match(q, syns)
                if matched_syn:
                    filters['os'] = canon
                    break
            else:
                if any(s in q for s in syns):
                    filters['os'] = canon
                    break

    # Customer type detection
    for canon, syns in CUSTOMER_SYNONYMS.items():
        if USE_FUZZY_MATCHING:
            matched_syn = fuzzy_match(q, syns)
            if matched_syn:
                filters['customer_type'] = canon
                break
        else:
            if any(s in q for s in syns):
                filters['customer_type'] = canon
                break

    # Network/VPN context
    if re.search(r'\bvpn\b', q):
        filters.setdefault('network', 'VPN')
        filters.setdefault('stage', 'network')

    # Error codes
    if ec := re.search(r'\b(ERR_[A-Z_]+|\d{3})\b', query, re.IGNORECASE):
        filters['error_code'] = ec.group(1)

    # Time context
    if re.search(r'\b(today|recent|just started)\b', q):
        filters['time_context'] = 'recent'
    elif re.search(r'\b(always|constantly|persistent)\b', q):
        filters['time_context'] = 'persistent'

    # Generic stage inference
    if 'stage' not in filters:
        if 'performance' in q and 'loading' in q:
            filters['stage'] = 'post-login'
        elif any(x in q for x in ['login failure', 'login issues']):
            filters['stage'] = 'SSO-redirect' if 'sso' in q else 'authentication'
        elif 'captcha' in q:
            filters['stage'] = 'captcha'
        elif 'form' in q:
            filters['stage'] = 'post-login'
        elif any(x in q for x in ['lockout', 'locked']):
            filters['stage'] = 'pre-login'
        elif 'reset' in q:
            filters['stage'] = 'password-reset'
        elif 'oauth' in q:
            filters['stage'] = 'consent'

    return filters