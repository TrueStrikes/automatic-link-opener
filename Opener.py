import requests
import json
import subprocess
import time
from colorama import init, Fore

# Initialize colorama to support colored text in the console
init()

# Change the browser path here as needed
BROWSER_PATH = r'yourbrowserpath'

# Set to keep track of opened links
opened_links = set()

def open_in_browser(url):
    subprocess.run([BROWSER_PATH, url], shell=True)

def retrieve_latest_message(channelid):
    headers = {
        'authorization': 'yourtoken'
    }
    r = requests.get(f'https://discord.com/api/v8/channels/{channelid}/messages', headers=headers)
    messages = json.loads(r.text)
    
    if not isinstance(messages, list) or len(messages) == 0:
        return

    latest_message = messages[0]  # The latest message is the first in the list

    embeds = latest_message.get('embeds')
    if embeds:
        for embed in embeds:
            roblox_url = embed.get('url')
            if roblox_url and 'roblox.com/catalog/' in roblox_url and roblox_url not in opened_links:
                opened_links.add(roblox_url)  # Add the link to the set
                print(f"{Fore.RED}Opened a link: {roblox_url}{Fore.RESET}")
                open_in_browser(roblox_url)

# Change the channel ID here as needed
channel_id = '1094291863332192376'

# Set the loop to run indefinitely
while True:
    retrieve_latest_message(channel_id)
    time.sleep(0.2)  # Add a wait time of 0.2 seconds before the next iteration
