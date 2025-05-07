import os

# Model configurations
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
DATASET_PATH = "support_tickets_dataset.json"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Synonym maps
BROWSER_SYNONYMS = {
    "safari": ["safari", "mobile safari", "safari mobile"],
    "chrome": ["chrome", "google chrome"],
    "firefox": ["firefox", "mozilla firefox"],
    "edge": ["edge", "microsoft edge"],
    "brave": ["brave"],
    "opera": ["opera"],
    "samsung internet": ["samsung internet", "samsung browser"],
    "in-app browser": ["in-app browser", "in app browser", "app browser"],
    "internet explorer 11": ["internet explorer", "ie11", "ie 11", "internet explorer 11"],
    "vivaldi": ["vivaldi"],
    "duckduckgo browser": ["duckduckgo browser", "duck duck go", "ddg browser"],
    "tor browser": ["tor", "tor browser"],
}

OS_SYNONYMS = {
    "macos ventura": ["macos ventura", "ventura", "mac os ventura", "macos 13"],
    "macos monterey": ["macos monterey", "monterey", "macos 12"],
    "macos sonoma": ["macos sonoma", "sonoma"],
    "windows 10": ["windows 10", "win10", "win 10"],
    "windows 11": ["windows 11", "win11", "win 11"],
    "linux ubuntu": ["ubuntu", "linux ubuntu"],
    "linux mint": ["mint", "linux mint"],
    "ios 15": ["ios 15", "ios15", "iphone os 15"],
    "ios 16": ["ios 16", "ios16"],
    "android 13": ["android 13", "android13"],
    "chrome os": ["chrome os", "chromebook"],
    "windows": ["windows", "win"],
}

CUSTOMER_SYNONYMS = {
    "enterprise": ["enterprise", "corp", "corporate"],
    "mixed": ["mixed"],
    "smb": ["smb", "small business", "small & medium", "small & medium business"],
    "marketing": ["marketing"],
    "individual": ["individual", "personal"],
    "education": ["education", "edu", "student"],
    "government": ["government", "gov"],
    "finance": ["finance", "financial", "banking"],
    "retail": ["retail"],
    "healthcare": ["healthcare", "health care"],
    "non-profit": ["non-profit", "nonprofit", "not for profit"],
    "technology": ["technology", "tech"],
}

STAGE_SYNONYMS = {
    'pre-login': ['pre-login', 'before login', 'initial load'],
    'captcha': ['captcha', 'challenge'],
    'post-login': ['post-authentication', 'after login', 'dashboard', 'post-login'],
    'consent': ['consent', 'oauth consent', 'consent stuck'],
    '2FA': ['two-factor', '2fa', '2 factor'],
    'loading': ['spinner', 'infinite loading']
}

exact_match_boost = {
    "session": ["session", "timeout", "session expired", "cookie", "cookie issues", "kicked out", "randomly kicked out"],
    "authentication": ["login", "auth", "sso", "oauth", "password reset", "verification", "two-factor", "2fa", "account locked", "email verification failure"],
    "network": ["vpn", "firewall", "proxy", "network error", "redirect", "err_network", "certificate error"],
    "captcha": ["captcha", "captcha missing"],
    "ui": ["blank white page", "ui broken", "feature not working", "form submission failure"],
    "performance": ["performance slow", "slow", "loading", "lag", "infinite loading"],
    "error_codes": ["403 error", "404 error", "500 error"],
    "form": ["form submission failure", "form error", "submission"],
    "sync": ["data sync", "sync issue", "data sync issue"],
    "reset": ["reset", "resend verification email", "password reset"],
    "blank_page": ["blank white page", "white page", "blank page"],
    "oauth": ["oauth", "consent", "consent stuck"],
    "vpn": ["vpn", "network error", "err_network"],
    "two_factor": ["2fa", "two-factor", "two factor"],
}

BROWSER_MAP = [
    (r'\bsafari[\s-]?(\d+\.\d+)?\b', 'Safari', 1),
    (r'\bchrome[\s-]?(\d+\.\d+)?\b', 'Chrome', 1),
    (r'\b(?:firefox|ff)[\s-]?(\d+(?:\.\d+)?)?\b', 'Firefox', 1),
    (r'\b(?:edge|microsoft edge)[\s-]?(\d+\.\d+)?\b', 'Edge', 1),
    (r'\bbrave[\s-]?(\d+\.\d+)?\b', 'Brave', 1),
    (r'\bopera[\s-]?(\d+\.\d+)?\b', 'Opera', 1),
    (r'\bsamsung internet[\s-]?(\d+\.\d+)?\b', 'Samsung Internet', 1),
    (r'\bin-app browser[\s-]?(\d+\.\d+)?\b', 'In-App Browser', 1),
    (r'\b(?:internet explorer|ie)[\s-]?11\b', 'Internet Explorer 11', None),
    (r'\bvivaldi[\s-]?(\d+\.\d+)?\b', 'Vivaldi', 1),
    (r'\b(?:duckduckgo|ddg)[\s-]?browser[\s-]?(\d+\.\d+)?\b', 'DuckDuckGo Browser', 1),
    (r'\btor[\s-]?browser[\s-]?(\d+\.\d+)?\b', 'Tor Browser', 1),
]