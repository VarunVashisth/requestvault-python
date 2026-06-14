from requestvault import RequestVault
import requests , time

RequestVault.init(
    api_key="",
    )

requests.post(
    "https://httpbin.org/post",
    json={
        "name": "Varun",
        "password": "123"
    }
)
time.sleep(5)

print(RequestVault.status())
wrtwRW