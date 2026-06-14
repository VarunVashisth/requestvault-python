from urllib.parse import urlparse

from ..config import Config


def normalize_rule(rule: str) -> str:
    """
    Normalize user rules.

    Examples:
    api.stripe.com
    https://api.stripe.com/v1/
    """

    return rule.strip().rstrip("/")


def is_domain_rule(rule: str) -> bool:
    return "://" not in rule


def match_rule(url: str, rule: str) -> bool:
    """
    Supports:

    api.stripe.com
    https://api.stripe.com/v1
    """

    parsed = urlparse(url)

    hostname = (parsed.hostname or "").lower()

    rule = normalize_rule(rule)

    # DOMAIN MATCH
    if is_domain_rule(rule):
        return hostname == rule.lower()

    # PREFIX MATCH
    return url.rstrip("/").startswith(rule)


def is_excluded(url: str) -> bool:

    for rule in Config.exclude_urls:
        try:
            if match_rule(url, rule):
                return True
        except Exception:
            continue

    return False


def is_included(url: str) -> bool:

    if not Config.include_urls:
        return True

    for rule in Config.include_urls:
        try:
            if match_rule(url, rule):
                return True
        except Exception:
            continue

    return False


def should_capture(url: str) -> bool:
    """
    Decision order:

    1. exclude wins
    2. include check
    """

    if is_excluded(url):
        return False

    return is_included(url)
