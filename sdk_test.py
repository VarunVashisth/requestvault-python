from requestvault import RequestVault
import requests , time

RequestVault.init(
    api_key="rv_o56NwCIz9s-JZHX1jl3wVbIIp_81QEaDV2V_h5MYPGs",
    capture_headers=False,
    debug=True,
    )



try:
        requests.get("https://httpbin.org/get")
except:
    pass 

time.sleep(5)


