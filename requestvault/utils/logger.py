from ..config import Config

def log(message):

    if Config.debug:
        print(f"[RequestVault] {message}")