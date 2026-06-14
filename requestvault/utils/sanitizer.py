import json
from datetime import datetime, date
from decimal import Decimal



SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "token",
    "secret",
    "api-key",
    "apikey",
    "auth",
    "jwt",
}

SENSITIVE_FIELDS = {
    "password",
    "token",
    "secret",
    "auth",
    "credential",
    "jwt",
    "cookie",
    "api_key",
    "private_key",
    "secret_key",
}


def sanitize_body(data):

    if data is None:
        return None

    if isinstance(data, (bytes, bytearray)):

        try:
            decoded = data.decode("utf-8")

            try:
                return sanitize_body(
                    json.loads(decoded)
                )

            except Exception:
                return decoded

        except Exception:
            return "[BINARY_DATA]"

    if isinstance(data, (datetime, date)):
        return data.isoformat()

    if isinstance(data, Decimal):
        return float(data)

    if isinstance(data, dict):

        cleaned = {}

        for key, value in data.items():

            key_str = str(key)
            lower_key = key_str.lower()

            if any(
                pattern in lower_key
                for pattern in SENSITIVE_FIELDS
            ):
                cleaned[key_str] = "[REDACTED]"

            else:
                cleaned[key_str] = sanitize_body(value)

        return cleaned

    if isinstance(data, list):
        return [sanitize_body(item) for item in data]

    if isinstance(data, tuple):
        return [sanitize_body(item) for item in data]

    if isinstance(data, set):
        return [sanitize_body(item) for item in data]

    if isinstance(data, str):

        stripped = data.strip()

        if (
            stripped.startswith("{")
            or stripped.startswith("[")
        ):
            try:
                parsed = json.loads(data)

                return sanitize_body(parsed)

            except Exception:
                pass

        return data

    if isinstance(data, (bool, int, float)):
        return data

    try:
        return str(data)

    except Exception:
        return "[UNSERIALIZABLE_OBJECT]"


def sanitize_headers(headers):

    if not headers:
        return None

    cleaned = {}

    for key, value in headers.items():

        key_str = str(key)
        lower_key = key_str.lower()

        if any(
            pattern in lower_key
            for pattern in SENSITIVE_HEADERS
        ):
            cleaned[key_str] = "[REDACTED]"
            continue

        if value is None:
            cleaned[key_str] = None

        elif isinstance(
            value,
            (bool, int, float, str)
        ):
            cleaned[key_str] = value

        elif isinstance(
            value,
            (bytes, bytearray)
        ):
            try:
                decoded = value.decode("utf-8")

                try:
                    cleaned[key_str] = json.loads(decoded)
    
                except Exception:
                    cleaned[key_str] = decoded

            except Exception:
                cleaned[key_str] = "[BINARY_DATA]"

        else:
            try:
                cleaned[key_str] = repr(value)
            except Exception:
                cleaned[key_str] = "[UNSERIALIZABLE_HEADER]"

    return cleaned




def prepare_body(data):
    return  sanitize_body(data)
    


def prepare_headers(headers):
    return  sanitize_headers(headers)
    