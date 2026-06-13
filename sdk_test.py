from requestvault import RequestVault
import requests , time

RequestVault.init(
    api_key="rv_fWhHBn63eLTdAZBGm1-YjUAMpZwVO7tXhBcnOlvHOXM",
    )

requests.get(
    "https://httpbin.org/get"
)
time.sleep(5)

print(RequestVault.status())
