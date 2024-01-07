import sys
import time
from datetime import datetime, timedelta
import random

import requests

from car_factory import CarFactory


def get_tunnels():
    tunnels = "http://localhost:5000/tunnels"
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(tunnels, headers=headers)
        return response
    except requests.exceptions.ConnectionError:
        print("Server unavailable. Quiting...")
        sys.exit(1)


if __name__ == "__main__":
    print("Generating traffic...")

    r = get_tunnels()
    all_tunnels = r.json()
    print(all_tunnels)

    while True:
        selected_tunnel = random.choice(all_tunnels)

        tunnel_id = selected_tunnel['id']
        tunnel_length = selected_tunnel['length']
        tunnel_name = selected_tunnel['name']

        start_time = datetime.strptime('2024-01-05 10:00', '%Y-%m-%d %H:%M')
        current_time = start_time + timedelta(hours=random.randint(1, 240))

        print(f"Sending traffic through tunnel name: {tunnel_name}, id: {tunnel_id}, length: {tunnel_length}")

        print(f"Producing car at: {current_time}")
        factory = CarFactory(start_time=current_time)
        factory.run(tunnel_id=tunnel_id, tunnel_length=tunnel_length)
        print("Car went through... sleeping for 3 seconds")
        time.sleep(3)

