from .config import Config
from .instrumentation_httpx import instrument_httpx
from .instrumentation import instrument_requests 
from .sender import start_worker
from .utils.queue import event_queue
from .filters.validators import (validate_api_key , validate_url_rules , validate_sample_rate)
from .sdk_state import sdk_status


class RequestVault:

    @staticmethod
    def init(
        api_key,
        server_url = "http://localhost:8000",
        include_urls=None,
        exclude_urls=None,
        sample_rate=1.0,
        capture_headers=True,
        capture_request_body=True,
        capture_response_body=True,
        debug=False
    ):

        try:

            sdk_status["healthy"] = True
            sdk_status["enabled"] = True
            sdk_status["errors"] = []

            Config.debug = debug
            Config.server_url = server_url

            Config.api_key = validate_api_key(
                api_key
            )

            Config.include_urls = validate_url_rules(
                include_urls,
                "include_urls"
            )

            Config.exclude_urls = validate_url_rules(
                exclude_urls,
                "exclude_urls"
            )
            Config.sample_rate = validate_sample_rate(sample_rate)
            Config.capture_headers = bool(capture_headers)
            Config.capture_request_body = bool(capture_request_body)
            Config.capture_response_body = bool(capture_response_body)

            if not sdk_status["enabled"]:
                return

            if not getattr(
                Config,
                "worker_started",
                False
            ):
                start_worker()
                Config.worker_started = True

            if not getattr(
                Config,
                "instrumented",
                False
            ):
                instrument_httpx()
                instrument_requests()
                Config.instrumented = True

        except Exception as e:

            sdk_status["healthy"] = False
            sdk_status["enabled"] = False

            sdk_status["errors"].append(
                f"Initialization failed: {e}"
            )

            if debug:
                print(
                    f"[RequestVault] Initialization failed: {e}"
                )