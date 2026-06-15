

from requestvault import RequestVault
import requests
import time

RequestVault.init(
    api_key="rv_test",
    debug=True
)

print("Creating test traffic...")

# Success GET
try:
    requests.get("https://httpbin.org/get")
except:
    pass

# Success POST
try:
    requests.post(
        "https://httpbin.org/post",
        json={"name": "varun"}
    )
except:
    pass

# 404
try:
    requests.get(
        "https://httpbin.org/status/404"
    )
except:
    pass

# 500
try:
    requests.get(
        "https://httpbin.org/status/500"
    )
except:
    pass

# Timeout / failed request
try:
    requests.get(
        "https://this-domain-does-not-exist-123456.com",
        timeout=2
    )
except:
    pass



print("Waiting for SDK worker flush...")

time.sleep(10)

print("Done")