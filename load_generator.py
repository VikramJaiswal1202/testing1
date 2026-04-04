import requests
import time
import sys

URL = "http://localhost:8000/api/simulate"

def create_load():
    print(f"Starting continuous POST requests to {URL}")
    success_count = 0
    error_count = 0
    
    while True:
        try:
            start_time = time.time()
            response = requests.post(URL, json={"data": "test payload"}, timeout=10)
            latency = time.time() - start_time
            if response.status_code == 200:
                success_count += 1
                delay_applied = response.json().get('delay_applied_ms', 0)
                print(f"[{success_count}] OK in {latency:.3f}s (Injected delay: {delay_applied}ms)", end="\r")
            else:
                error_count += 1
                print(f"\n[error] Received status code {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"\n[error] Request failed: {e}")
            
        time.sleep(1) # Send 1 request per second

if __name__ == "__main__":
    try:
        create_load()
    except KeyboardInterrupt:
        print("\nStopping load generator...")
        sys.exit(0)
