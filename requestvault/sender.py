import threading
import requests
from .utils.queue import event_queue
from .config import Config
from .sdk_state import sdk_status
from .utils.logger import log


def start_worker():

    thread = threading.Thread(
        target=worker,
        daemon=True,
        name="RequestVaultWorker"
    )

    thread.start()

    log("Worker started")


def worker():

    session = requests.Session()

    while True:

        item = event_queue.get()

        try:

            response = session.post(
                f"{Config.server_url}/capture",
                json=item,
                timeout=5
            )

            if response.status_code == 401:

                sdk_status["healthy"] = False

                sdk_status["errors"].append(
                    "Invalid API key"
                )

                log(
                    "Capture rejected: Invalid API key"
                )

            elif response.status_code >= 500:

                sdk_status["healthy"] = False

                sdk_status["errors"].append(
                    f"Server error: {response.status_code}"
                )

                log(
                    f"Server error: {response.status_code}"
                )

            else:

                sdk_status["healthy"] = True

                log(
                    f"Captured request ({response.status_code})"
                )

        except requests.Timeout:

            sdk_status["healthy"] = False

            sdk_status["errors"].append(
                "Capture timeout"
            )

            log(
                "Capture timeout"
            )

        except requests.ConnectionError:

            sdk_status["healthy"] = False

            sdk_status["errors"].append(
                "Capture server unreachable"
            )

            log(
                "Capture server unreachable"
            )

        except Exception as e:

            sdk_status["healthy"] = False

            sdk_status["errors"].append(
                str(e)
            )

            log(
                f"Worker error: {e}"
            )

        finally:

            event_queue.task_done()