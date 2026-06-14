class Config:
    api_key = None
    server_url = "http://localhost:8000"
    healthy = True
    last_error = None

    include_urls = []
    exclude_urls = []

    debug=False

    instrumented = False
    worker_started = False
    sample_rate = 1.0

    capture_headers = True
    
    capture_request_body = True
    capture_response_body = True

    max_body_size = 25000

    
    

