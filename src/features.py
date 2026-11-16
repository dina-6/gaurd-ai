import ipaddress
import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = {
    "login", "verify", "account", "update", "secure", "bank", "signin",
    "password", "confirm", "wallet", "billing", "support", "free", "gift",
}

def extract_features(url: str) -> dict:
    """Extract explainable lexical/host features. Does not visit the URL."""
    raw = str(url).strip()
    candidate = raw if "://" in raw else "http://" + raw
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    path = parsed.path or ""
    lower = raw.lower()

    try:
        ipaddress.ip_address(host)
        uses_ip = 1
    except ValueError:
        uses_ip = 0

    labels = host.split(".") if host else []
    return {
        "url_length": len(raw),
        "hostname_length": len(host),
        "path_length": len(path),
        "count_dots": raw.count("."),
        "count_hyphens": raw.count("-"),
        "count_at": raw.count("@"),
        "count_question": raw.count("?"),
        "count_equal": raw.count("="),
        "count_percent": raw.count("%"),
        "count_digits": sum(ch.isdigit() for ch in raw),
        "count_slashes": raw.count("/"),
        "https_token_in_text": int("https" in lower),
        "has_https_scheme": int(parsed.scheme.lower() == "https"),
        "has_ip_address": uses_ip,
        "subdomain_count": max(0, len(labels) - 2),
        "has_port": int(parsed.port is not None),
        "has_punycode": int("xn--" in host),
        "has_double_slash_path": int("//" in path),
        "suspicious_word_count": sum(word in lower for word in SUSPICIOUS_WORDS),
        "has_shortener_hint": int(any(s in host for s in ("bit.ly", "tinyurl", "t.co", "goo.gl"))),
    }

def explain_url(url: str) -> list[str]:
    """Human-readable indicators; these are clues, not proof."""
    f = extract_features(url)
    notes = []
    if f["has_ip_address"]:
        notes.append("The hostname is an IP address rather than a regular domain.")
    if f["count_at"]:
        notes.append("The URL contains an @ symbol, which can make the real destination confusing.")
    if f["subdomain_count"] >= 3:
        notes.append("The URL contains several subdomain levels.")
    if f["suspicious_word_count"]:
        notes.append("The URL contains words commonly used in account or payment lures.")
    if f["has_punycode"]:
        notes.append("The domain uses punycode; inspect it carefully for look-alike characters.")
    if f["has_shortener_hint"]:
        notes.append("The hostname resembles a URL-shortening service, which hides the final destination.")
    if f["has_https_scheme"]:
        notes.append("HTTPS is present, but HTTPS alone does not prove a site is legitimate.")
    else:
        notes.append("The URL does not use HTTPS.")
    if not notes:
        notes.append("No obvious lexical warning signs were found. This does not guarantee safety.")
    return notes
