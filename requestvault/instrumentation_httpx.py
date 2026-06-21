import httpx
import time
import queue

from .utils.sanitizer import prepare_body, prepare_headers
from .utils.queue import event_queue
from .config import Config
from .filters.url_filter import should_capture
from .filters.sampling import should_sample
from .sdk_state import sdk_status
from .utils.logger import log
from .utils.size_limit import limit_size
from .instrumentation_ai import tag_ai_request

original_send = httpx.Client.send


def wrapper(
    self,
    request,
    *args,
    **kwargs
):

    url = str(request.url)
    method = request.method

    print("HTTPX HIT", method, url)

    if not sdk_status["enabled"]:
        return original_send(
            self,
            request,
            *args,
            **kwargs
        )

    if "/capture" in url:
        return original_send(
            self,
            request,
            *args,
            **kwargs
        )

    if not should_capture(url):
        log(f"[SKIPPED] {method} {url}")
        return original_send(
            self,
            request,
            *args,
            **kwargs
        )

    if not should_sample():

        log(
            f"[SAMPLED OUT] {method} {url}"
        )

        return original_send(
            self,
            request,
            *args,
            **kwargs
        )

    start = time.perf_counter()

    try:

        response = original_send(
            self,
            request,
            *args,
            **kwargs
        )

        elapsed_ms = int(
            (time.perf_counter() - start) * 1000
        )

        try:
            response_body = response.json()
        except Exception:
            response_body = response.text

        if Config.capture_headers:

            try:
                request_headers = prepare_headers(
                    dict(request.headers)
                )
            except Exception:
                request_headers = {}

            try:
                response_headers = prepare_headers(
                    dict(response.headers)
                )
            except Exception:
                response_headers = {}

        else:
            request_headers = None
            response_headers = None

        if Config.capture_request_body:

            try:
                request_body = prepare_body(
                    request.content
                )

                request_body = limit_size(
                    request_body
                )

            except Exception:
                request_body = None

        else:
            request_body = None

        if Config.capture_response_body:

            try:
                response_body = prepare_body(
                    response_body
                )

                response_body = limit_size(
                    response_body
                )

            except Exception:
                response_body = None

        else:
            response_body = None

        payload = {
            "api_key": Config.api_key,

            "method": method,

            "useragent": request_headers.get(
                "User-Agent"
            ) if request_headers else None,

            "endpoint": url,

            "status_code": response.status_code,
            "response_time_ms": elapsed_ms,

            "request_headers": request_headers,
            "response_headers": response_headers,

            "request_body": request_body,
            "response_body": response_body,
        }

        payload = tag_ai_request(
            payload,
            response_body
        )

        try:

            log(
                f"[CAPTURED]{method} {url}"
            )

            event_queue.put_nowait(
                payload
            )

        except queue.Full:

            log(
                "Queue full. Dropping event."
            )

        return response

    except Exception as e:

        elapsed_ms = int(
            (time.perf_counter() - start) * 1000
        )

        try:

            payload = {
                "api_key": Config.api_key,

                "method": method,
                "endpoint": url,

                "status_code": 0,
                "response_time_ms": elapsed_ms,

                "error": type(e).__name__,
                "error_message": str(e),

                "request_headers": {},
                "response_headers": {},

                "request_body": None,
                "response_body": None,
            }

            event_queue.put_nowait(
                payload
            )

        except Exception as capture_error:

            log(
                f"Failed to capture request: {capture_error}"
            )

        raise


def instrument_httpx():
    httpx.Client.send = wrapper