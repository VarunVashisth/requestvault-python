# RequestVault

Monitor every outgoing API request from your Python applications with zero boilerplate.

RequestVault is a developer observability tool that automatically captures outgoing HTTP requests made through Python applications and provides real-time analytics through a centralized dashboard.

---

## Features

* Automatic request tracking
* Zero-code request monitoring
* Real-time analytics dashboard
* Request performance insights
* Status code monitoring
* Error tracking
* API usage visibility
* Simple SDK integration

---

## Installation

```bash
pip install requestvault
```

---

## Getting Started

### 1. Create a RequestVault Account

Sign up on the RequestVault dashboard and generate your API key.

---

### 2. Initialize the SDK

```python
from requestvault import init

init(
    api_key="rv_your_api_key_here"
)
```

That's it.

Any outgoing requests made using the `requests` library will be automatically monitored.

---

## Example

```python
from requestvault import init
import requests

init(
    api_key="rv_your_api_key_here"
)

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1"
)

print(response.status_code)
```

The request will automatically appear inside your RequestVault dashboard.

---

## What Gets Captured

RequestVault collects:

* Request URL
* HTTP Method
* Response Status Code
* Response Time
* Timestamp
* Request Headers (configurable)
* Response Headers (configurable)

---

## Dashboard Analytics

The RequestVault dashboard provides:

* Total requests
* Success rate
* Error tracking
* Response time analysis
* Request history
* Endpoint insights

---

## Security

RequestVault is designed with security in mind.

Recommended practices:

* Never expose your API key publicly.
* Store API keys in environment variables.
* Rotate API keys regularly.
* Use separate API keys for development and production environments.

Example:

```python
import os

from requestvault import init

init(
    api_key=os.getenv("REQUESTVAULT_API_KEY")
)
```

---

## Requirements

* Python 3.10+
* requests

---

## Troubleshooting

### Requests not appearing in dashboard

Verify:

* SDK is initialized before making requests.
* API key is valid.
* Backend endpoint is reachable.
* Internet connection is available.

---

## Version

Current Version:

```text
0.1.0b1
```

---

## Roadmap

Planned features:

* SDK configuration options
* Custom event tracking
* Team workspaces
* Alerting system
* Advanced filtering
* Export capabilities
* Additional language SDKs

---

## Support

If you encounter issues or have feature requests, please open an issue on the GitHub repository.

---

Built for developers who want visibility into their application's API activity without adding unnecessary complexity.
