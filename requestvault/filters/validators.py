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