import discord
import subprocess

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Watching your channel for links.')

@client.event
async def on_message(message):
    if message.channel.id == your_channel_id:
        if len(message.embeds) > 0:
            for embed in message.embeds:
                if embed.url:
                    link = embed.url
                    browser = r"your_broswer_executable_path"
                    subprocess.run([browser, link], shell=True)

client.run('Yourbottoken')
