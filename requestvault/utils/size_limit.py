import json

from ..config import Config


def limit_size(data):

    if data is None:
        return None

    try:

        text = json.dumps(
            data,
            default=str,
            ensure_ascii=False
        )

    except Exception:

        text = str(data)

    max_size = Config.max_body_size

    if len(text) <= max_size:
        return data

    return {
        "truncated": True,
        "original_size": len(text),
        "preview_size": max_size,
        "preview": text[:max_size]
    }