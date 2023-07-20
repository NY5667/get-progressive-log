import requests
import time
import json

config_file = "configurations.json"

def check_response(config):
    baseUrlMs = config['baseUrlMs']
    bearer_token = config['bearerToken']
    
    url = baseUrlMs + "/servicemanager/msModule/getProgressiveLog"

    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.post(url, headers=headers)
    data = response.json()
    point = data["data"]["point"]
    message = data["data"]["message"]
    print(message)
    print()

    if point == 100:
        print(f"Configuration: {config['name']} - Point is 100 - Success!")
    else:
        print(f"Configuration: {config['name']} - Point: {point}")
    print()

def read_configurations():
    with open(config_file) as file:
        configurations = json.load(file)
    return configurations

configurations = read_configurations()

while True:
    for config in configurations:
        check_response(config)
    time.sleep(5)  # Pause for 5 seconds before checking again

while True:
    check_response()
    time.sleep(5)  # Pause for 60 seconds before making the next request
