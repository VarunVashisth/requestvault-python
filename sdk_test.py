from requestvault import RequestVault
import requests , time

RequestVault.init(
    api_key="",
    )

requests.get(
    "https://httpbin.org/get"
)
time.sleep(5)

print(RequestVault.status())
