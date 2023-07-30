import requests
import json
import webbrowser
import os
import time
from colorama import init, Fore

# Initialize colorama to support colored text in the console
init()

# Set to keep track of opened links
opened_links = set()

def send_discord_webhook(webhook_url, message):
    data = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code != 204:
        print(f"Failed to send webhook. Status code: {response.status_code}")

def retrieve_latest_message(channel_id, token, webhook_url):
    headers = {
        'authorization': token
    }
    params = {
        'limit': 1
    }
    r = requests.get(f'https://discord.com/api/v8/channels/{channel_id}/messages', headers=headers, params=params)
    messages = json.loads(r.text)
    
    if not isinstance(messages, list) or len(messages) == 0:
        return

    latest_message = messages[0]  # The latest message is the first in the list

    content = latest_message.get('content', '').lower()
    if 'free item yo' in content:
        roblox_links = find_roblox_links(content)
        for link in roblox_links:
            if link not in opened_links:
                opened_links.add(link)  # Add the link to the set
                message_to_send = "Opened a link: " + link
                send_discord_webhook(webhook_url, message_to_send)
                print(f"{Fore.RED}{message_to_send}{Fore.RESET}")
                open_in_browser(link)

def open_in_browser(url):
    webbrowser.open(url, new=0, autoraise=True)

def find_roblox_links(text):
    import re
    return re.findall(r'https?://(?:www\.)?roblox\.com/catalog/\d+', text)

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print("Config file 'config.json' not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format in 'config.json'.")
        return None

def main():
    config = load_config()
    if config is None:
        return

    channel_id = config.get('channel_id')
    webhook_url = config.get('webhook_url')
    token = config.get('token')

    if not channel_id or not webhook_url or not token:
        print("Missing required variables in 'config.json'.")
        return

    # Clear the console and print "The bot is working, there's just nothing to open" in yellow
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.YELLOW}The bot is working, there's just nothing to open{Fore.RESET}")

    # Set the loop to run indefinitely with a 0.2 seconds wait
    while True:
        retrieve_latest_message(channel_id, token, webhook_url)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
