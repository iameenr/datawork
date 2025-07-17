import requests
import json
import time
import random

EVENT_COLLECTOR_URL = "http://event-collector:8000/events"

EVENT_TYPES = ["page_view", "add_to_cart", "purchase"]

while True:
    event = {
        "event_type": random.choice(EVENT_TYPES),
        "product_id": str(random.randint(1, 10)),
        "user_id": str(random.randint(1, 500)),
    }
    try:
        requests.post(EVENT_COLLECTOR_URL, json=event)
        print(f"Sent event: {event}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending event: {e}")
    time.sleep(random.uniform(0.5, 2.0))
