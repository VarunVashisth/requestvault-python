from ..sdk_state import sdk_status
from ..utils.logger import log


def disable_sdk(reason):

    sdk_status["healthy"] = False
    sdk_status["enabled"] = False

    sdk_status["errors"].append(reason)

    log(reason)


def validate_api_key(api_key):

    if not api_key:

        disable_sdk(
            "API key missing. SDK disabled."
        )

        return None

    return api_key


def validate_url_rules(rules, name):

    if rules is None:
        return []

    if not isinstance(rules, list):

        log(
            f"{name} must be a list. Ignoring."
        )

        return []

    valid_rules = []

    for rule in rules:

        if not isinstance(rule, str):

            log(
                f"Ignoring invalid {name} rule: {rule}"
            )

            continue

        rule = rule.strip()

        if not rule:
            continue

        valid_rules.append(rule)

    return valid_rules

def validate_sample_rate(rate):

    try:

        rate = float(rate)

    except Exception:

        log(
            "Invalid sample_rate. Using 1.0"
        )

        return 1.0

    if rate < 0:
        return 0.0

    if rate > 1:
        return 1.0

    return rate


def validate_max_body_size(size):

    try:
        size = int(size)

    except Exception:

        log(
            "Invalid max_body_size. Using 10000."
        )

        return 10000

    if size < 100:
        return 100

    return size