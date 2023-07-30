import requests
import json
import webbrowser
import time
from colorama import init, Fore

# Initialize colorama to support colored text in the console
init()

# Set to keep track of opened links
opened_links = set()

# Replace 'YOUR_WEBHOOK_URL_HERE' with your actual webhook URL
YOUR_WEBHOOK_URL = 'yourwebhook'

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

def retrieve_latest_message(channelid):
    headers = {
        'authorization': 'yourtoken'
    }
    params = {
        'limit': 1
    }
    r = requests.get(f'https://discord.com/api/v8/channels/{channelid}/messages', headers=headers, params=params)
    messages = json.loads(r.text)
    
    if not isinstance(messages, list) or len(messages) == 0:
        return

    latest_message = messages[0]  # The latest message is the first in the list

    content = latest_message.get('content', '').lower()
    if 'roblox.com/catalog/' in content:
        roblox_links = find_roblox_links(content)
        for link in roblox_links:
            if link not in opened_links:
                opened_links.add(link)  # Add the link to the set
                message_to_send = "Opened a link: " + link
                send_discord_webhook(YOUR_WEBHOOK_URL, message_to_send)
                print(f"{Fore.RED}{message_to_send}{Fore.RESET}")
                open_in_browser(link)

    embeds = latest_message.get('embeds')
    if embeds:
        for embed in embeds:
            if 'roblox.com/catalog/' in embed.get('url', '') and embed.get('type') == 'rich':
                roblox_url = embed.get('url')
                if roblox_url and roblox_url not in opened_links:
                    opened_links.add(roblox_url)  # Add the link to the set
                    message_to_send = "Opened a link: " + roblox_url
                    send_discord_webhook(YOUR_WEBHOOK_URL, message_to_send)
                    print(f"{Fore.RED}{message_to_send}{Fore.RESET}")
                    open_in_browser(roblox_url)

def open_in_browser(url):
    webbrowser.open(url, new=0, autoraise=True)

def find_roblox_links(text):
    import re
    return re.findall(r'https?://(?:www\.)?roblox\.com/catalog/\d+', text)

# Change the channel ID here as needed
channel_id = '1094291863332192376'

# Clear the console and print "The bot is working, there's just nothing to open" in yellow
import os
os.system('cls' if os.name == 'nt' else 'clear')
print(f"{Fore.YELLOW}The bot is working, there's just nothing to open{Fore.RESET}")

# Set the loop to run indefinitely with a 0.2 seconds wait
while True:
    retrieve_latest_message(channel_id)
    time.sleep(0.2)
