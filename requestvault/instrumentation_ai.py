
import json
import logging
from typing import Optional, Dict, Any
from .config import Config
from .utils.logger import log

logger = logging.getLogger(__name__)

AI_PROVIDER_PATTERNS = {
    "openai": {
        "hosts": ["api.openai.com", "openai.com"],
        "paths": ["/v1/chat/completions", "/v1/completions", "/v1/embeddings"],
        "headers": ["authorization"],
    },
    "anthropic": {
        "hosts": ["api.anthropic.com", "anthropic.com"],
        "paths": ["/v1/messages", "/v1/complete"],
        "headers": ["authorization"],
    },
}


def detect_ai_provider(url: str, headers: Optional[Dict] = None) -> Optional[str]:

    url_lower = url.lower()

    for provider, patterns in AI_PROVIDER_PATTERNS.items():
        for host in patterns.get("hosts", []):
            if host in url_lower:
                return provider

        for path in patterns.get("paths", []):
            if path in url_lower:
                return provider

    return None


def extract_ai_metadata(
    url: str,
    request_body: Optional[Any] = None,
    response_body: Optional[Any] = None,
    response_headers: Optional[Dict] = None,
) -> Optional[Dict[str, Any]]:

    try:
        provider = detect_ai_provider(url)
        if not provider:
            return None

        metadata = {
            "ai_provider": provider,
            "ai_model": None,
            "ai_tokens": None,
            "ai_cost_estimate": None,
        }

        model = None
        if request_body:
            try:
                req_data = (
                    json.loads(request_body)
                    if isinstance(request_body, str)
                    else request_body
                )
                if isinstance(req_data, dict):
                    model = req_data.get("model")
            except Exception:
                pass

        if not model and response_body:
            try:
                resp_data = (
                    json.loads(response_body)
                    if isinstance(response_body, str)
                    else response_body
                )
                if isinstance(resp_data, dict):
                    model = resp_data.get("model")
            except Exception:
                pass

        metadata["ai_model"] = model

        tokens = None
        if response_body:
            try:
                resp_data = (
                    json.loads(response_body)
                    if isinstance(response_body, str)
                    else response_body
                )
                if isinstance(resp_data, dict) and "usage" in resp_data:
                    usage = resp_data["usage"]
                    tokens = {
                        "input": usage.get("prompt_tokens"),
                        "output": usage.get("completion_tokens"),
                        "total": usage.get("total_tokens"),
                    }
            except Exception:
                pass

        metadata["ai_tokens"] = tokens

        return metadata

    except Exception as e:
        logger.debug(f"Error extracting AI metadata: {e}")
        return None


def tag_ai_request(payload: Dict, response_body: Optional[Any] = None) -> Dict:
    """
    Add AI observability tags to the payload.

    Updates the tags array with AI-specific information.
    """
    try:

        
        if not isinstance(payload, dict):
            return payload

 
        ai_metadata = extract_ai_metadata(
            payload.get("endpoint", ""),
            payload.get("request_body"),
            response_body or payload.get("response_body"),
        )

        if ai_metadata:
 
            if "tags" not in payload:
                payload["tags"] = []

 
            if isinstance(payload["tags"], list):
                payload["tags"].extend([
                    "ai",
                    f"ai_{ai_metadata.get('ai_provider')}",
                ])

                if ai_metadata.get("ai_model"):
 
                    model_tag = (
                        ai_metadata["ai_model"]
                        .lower()
                        .replace("-", "_")
                        .replace(".", "_")
                    )
                    payload["tags"].append(f"model_{model_tag}")

 
            payload["ai_observability"] = ai_metadata

            tokens = ai_metadata.get("ai_tokens") or {}

            log(
                f"[AI] {ai_metadata.get('ai_provider')} "
                f"- {ai_metadata.get('ai_model')} "
                f"- Tokens: {tokens.get('total', 'N/A')}"
            )

    except Exception as e:
        logger.debug(f"Error tagging AI request: {e}")

    return payload
