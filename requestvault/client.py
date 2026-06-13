from .config import Config
from .instrumentation import instrument_requests 
from .sender import start_worker
from .utils.queue import event_queue

class RequestVault:

    @staticmethod
    def init(
        api_key,
        server_url="http://localhost:8000"
    ):
        
        Config.api_key = api_key
        Config.server_url = server_url

        start_worker()

        instrument_requests()
    
    @staticmethod
    def status() :

        return {
            "healthy":Config.healthy,
            "last_error":Config.last_error,
            "queue_size":event_queue.qsize(),
            "api_key_set": Config.api_key is not None
        }
