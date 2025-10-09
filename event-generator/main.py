import requests
import time
import random

URL = "http://event-collector:8000/events" # the url for the collector

EVENT_TYPES = ["page_view", "add_to_cart", "purchase"]

# main loop
while True:
    payload = {
        "event_type": random.choice(EVENT_TYPES),
        "product_id": str(random.randint(1, 10)),
        "user_id": str(random.randint(1, 500)),
    }
    try:
        # send it
        requests.post(URL, json=payload)
        print(f"sent: {payload}")
    except requests.exceptions.RequestException as e:
        print(f"coudnt send event: {e}") # typo here
    
    # wait a bit
    time.sleep(random.uniform(0.5, 2.0))