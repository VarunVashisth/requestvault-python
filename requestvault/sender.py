import threading
from .utils.queue import event_queue 
import requests
from .config import Config
def start_worker():
    thread = threading.Thread(
        target=worker,
        daemon=True
    )

    thread.start()

def worker():

    while True:

        item = event_queue.get()

        try:

            print("Sending...")
            print(type(item))
            print(item)

            response = requests.post(
                "http://localhost:8000/capture",
                json=item,
                timeout=5
            )

            print("Status:", response.status_code)
            print("Response:", response.text)

            if response.status_code == 401:
                Config.healthy = False
                Config.last_error = "Invalid API Key"

        except Exception as e:

            Config.healthy = False
            Config.last_error = str(e)

            print("WORKER ERROR:")
            print(type(e))
            print(e)
