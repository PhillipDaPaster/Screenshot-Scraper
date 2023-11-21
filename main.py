import os
import sys
import random
import time
import json
import string
from dhooks import Webhook

YELLOW, RESET = '\033[93m', '\033[0m'

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_and_send_url(hook, url_prefix, length=6):
    random_url = url_prefix + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    print(f'[{YELLOW}Success{RESET}] Printing "{random_url}"')
    hook.send(random_url)

def main(config):
    interval = int(config["interval"])
    webhook = Webhook(config["webhook"])
    loop_count = int(config["loop"]) if config["loop"] != "forever" else None
    url_prefix = config["url_prefix"]

    print(f"LoopConCurrent '{loop_count}' URL Every {interval} seconds | Prefix: '{url_prefix}'.")

    for _ in range(loop_count) if loop_count is not None else iter(int, 1):
        generate_and_send_url(webhook, url_prefix)
        time.sleep(interval)

if __name__ == "__main__":
    config_data = load_config('config.json')
    main(config_data)
