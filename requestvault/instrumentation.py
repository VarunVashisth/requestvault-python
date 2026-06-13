import requests
import time
import queue
from .utils.sanitizer import prepare_body , prepare_headers
from .utils.queue import event_queue
from .config import Config

original_request = requests.Session.request

sdk_status = {
    "healthy": True
}

def wrapper(
        self,
        method,
        url,
        **kwargs
):
 
    if "/capture" in url:
        return original_request(
            self,
            method,
            url,
            **kwargs
        )

    start = time.perf_counter()

    response = original_request(
        self,
        method,
        url,
        **kwargs
    )

    elapsed_ms = int(time.perf_counter() - start)*1000

    try:
        response_body = response.json()
    except Exception:
        response_body = response.text

    request_headers = prepare_headers(
    response.request.headers
    )
    
    response_headers = prepare_headers(
        response.headers
    )
    
    request_body = prepare_body(
        response.request.body
    )
    
    response_body = prepare_body(
        response_body
    )


    payload = {
    "api_key": Config.api_key,

    "method": method.upper(),
    "useragent": request_headers.get("User-Agent"),

    "endpoint": url,
    "status_code": response.status_code,
    "response_time_ms": elapsed_ms,

    "request_headers": request_headers,
    "response_headers": response_headers,

    "request_body": request_body,
    "response_body": response_body
    }
    
    print(payload)
    try:
      event_queue.put_nowait(payload)
    except queue.Full:
        pass

    return response



def instrument_requests():
    requests.Session.request = wrapper