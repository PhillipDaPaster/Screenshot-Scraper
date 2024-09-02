import os
import sys
import random
import time
import json
import string
import requests
from dhooks import Webhook

YELLOW, RED, RESET = '\033[93m', '\033[91m', '\033[0m'

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def check_url(url):
    try:
        response = requests.get(url)
        return response.status_code != 404
    except requests.RequestException as e:
        print(f'[{RED}Error{RESET}] Failed to check URL "{url}": {e}')
        return False

def generate_and_send_url(hook, url_prefix, config):

    str_length = int(config["str_length"])
    random_url = url_prefix + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(str_length))
    if check_url(random_url):
        print(f'[{YELLOW}Success{RESET}] URL is valid. Sending "{random_url}"')
        hook.send(random_url)
    else:
        print(f'[{RED}Failed{RESET}] URL is 404: "{random_url}"')

def main(config):
    interval = int(config["interval"])
    webhook = Webhook(config["webhook"])
    loop_count = int(config["loop"]) if config["loop"] != "forever" else None
    url_prefix = config["url_prefix"]

    print(f"LoopConCurrent '{loop_count}' URL Every {interval} seconds | Prefix: '{url_prefix}'.")

    for _ in range(loop_count) if loop_count is not None else iter(int, 1):
        generate_and_send_url(webhook, url_prefix, config)
        time.sleep(interval)

if __name__ == "__main__":
    config_data = load_config('config.json')
    main(config_data)
