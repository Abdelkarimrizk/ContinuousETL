import random
import time
import json
import string
import requests
from datetime import datetime, timezone

API_GATEWAY = "empty for now"
interval = 10 

pages = ["/home", "/products", "/cart", "/checkout", "/profile", "/about"]
device_types = ["desktop", "mobile", "tablet", "samsung fridge"]

# I mean, take a wild guess
def generate_user_id():
    return "u" + "".join(random.choices(string.digits, k=4))

# generates a random event that would be sent to aws
def generate_event():
    timestamp = datetime.now(timezone.utc).isoformat()
    return {
        "user_id": generate_user_id(),
        "event_type": "page_view",
        "page" : random.choice(pages),
        "device_type": random.choice(device_types),
        "timestamp": timestamp
    }


# function to send the events to the API gateway every interval(10) seconds
def send_event():
    while True:
        event = generate_event()
        json_data = json.dumps(event)
        try:
            response = requests.post(API_GATEWAY, data=json_data, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                print(f"Event sent successfully: {event}")
            else:
                print(f"Failed to send event: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error sending event: {e}")

        time.sleep(interval)

if __name__ == "__main__":
    send_event()
