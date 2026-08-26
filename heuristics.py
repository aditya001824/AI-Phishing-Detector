import re
from typing import Dict, List, Any
from urllib.parse import urlparse

# Suspicious TLDs frequently abused in phishing campaigns
SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".club", ".work", ".click", ".loan", ".tk", 
    ".ml", ".ga", ".cf", ".gq", ".buzz", ".cam", ".rest", ".fit"
}

# Known URL shortener domains
SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "buff.ly", 
    "ow.ly", "rebrand.ly", "cutt.ly", "goo.gl", "shorturl.at"
}

# High-urgency and financial trigger keywords
URGENCY_KEYWORDS = [
    "urgent", "immediately", "account suspended", "verify your account",
    "password reset", "security alert", "unauthorized access", "action required",
    "limited time", "suspended", "confirm identity", "bank alert"
]

FINANCIAL_KEYWORDS = [
    "lottery", "winner", "prize", "claim your", "free money",
    "transfer funds", "wire transfer", "inheritance", "million dollars",
    "bitcoin", "cryptocurrency", "gift card", "reward"
]


def extract_urls(text: str) -> List[str]:
    """Extract all HTTP/HTTPS and domain-like URLs from text."""
    url_pattern = r'(?:https?://|www\.)[^\s/$.?#].[^\s]*'
    return re.findall(url_pattern, text, re.IGNORECASE)


def analyze_urls(urls: List[str]) -> Dict[str, Any]:
    """Analyze extracted URLs for phishing indicators."""
    has_ip_url = False
    has_shortener = False
    suspicious_tld_found = []
    
    ip_pattern = re.compile(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    for url in urls:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        if ip_pattern.match(url):
            has_ip_url = True

        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            
            # Check domain against URL shorteners
            if hostname.lower() in SHORTENER_DOMAINS:
                has_shortener = True

            # Check TLD
            for tld in SUSPICIOUS_TLDS:
                if hostname.lower().endswith(tld):
                    suspicious_tld_found.append(tld)
        except Exception:
            continue

    return {
        "url_count": len(urls),
        "has_ip_address_url": has_ip_url,
        "has_shortened_url": has_shortener,
        "suspicious_tlds": list(set(suspicious_tld_found))
    }


def analyze_heuristics(text: str) -> Dict[str, Any]:
    """
    Perform heuristic security analysis on text message / email content.
    Returns detected risk factors and a heuristic risk score (0 to 100).
    """
    if not text:
        return {"risk_score": 0, "flags": [], "url_analysis": {}}

    text_lower = text.lower()
    flags = []
    score = 0

    # 1. URL Analysis
    urls = extract_urls(text)
    url_data = analyze_urls(urls)

    if url_data["has_ip_address_url"]:
        score += 35
        flags.append("Contains direct IP address URL (high phishing risk)")

    if url_data["has_shortened_url"]:
        score += 25
        flags.append("Contains shortened URL masking true destination")

    if url_data["suspicious_tlds"]:
        score += 20
        flags.append(f"Contains suspicious TLDs: {', '.join(url_data['suspicious_tlds'])}")

    if url_data["url_count"] > 3:
        score += 15
        flags.append(f"Excessive links detected ({url_data['url_count']} URLs)")

    # 2. Urgency and Threat Analysis
    matched_urgency = [kw for kw in URGENCY_KEYWORDS if kw in text_lower]
    if matched_urgency:
        score += min(len(matched_urgency) * 15, 30)
        flags.append(f"High-urgency language detected: '{', '.join(matched_urgency[:3])}'")

    # 3. Financial and Scam Keywords
    matched_financial = [kw for kw in FINANCIAL_KEYWORDS if kw in text_lower]
    if matched_financial:
        score += min(len(matched_financial) * 15, 30)
        flags.append(f"Financial bait / prize keywords: '{', '.join(matched_financial[:3])}'")

    # 4. Excessive Punctuation / Caps
    exclamations = text.count("!") + text.count("$$")
    if exclamations >= 3:
        score += 10
        flags.append("Excessive exclamation marks or dollar signs")

    risk_score = min(score, 100)
    risk_level = "LOW"
    if risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"

    return {
        "heuristic_score": risk_score,
        "risk_level": risk_level,
        "flags": flags,
        "url_analysis": url_data
    }
