from requestvault import RequestVault
import requests , time

RequestVault.init(
    api_key="rv_fWhHBn63eLTdAZBGm1-YjUAMpZwVO7tXhBcnOlvHOXM",
    exclude_urls= ["https://api.github.com"],
    debug=True
    )



try:
    requests.get(
        "https://httpbin.org/delay/10",
        timeout=1
    )
except:
    pass 

time.sleep(5)


