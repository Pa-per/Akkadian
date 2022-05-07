import json
import os

import aiohttp
import discord
import requests
from bs4 import BeautifulSoup

with open("config.json") as file:
    data = json.load(file)
    streaming = data["bot"]["status"]["streaming"]["boolean"]
    watching = data["bot"]["status"]["watching"]["boolean"]
    playing = data["bot"]["status"]["playing"]["boolean"]


async def load_cogs(client):
    for filename in os.listdir("commands"):
        if filename.endswith(".py"):
            await client.load_extension(f"commands.{filename[:-3]}")
            print(f"Loaded {filename[:-3]}")
    for filename in os.listdir("events"):
        if filename.endswith(".py"):
            await client.load_extension(f"events.{filename[:-3]}")
            print(f"Loaded {filename[:-3]}")


async def set_status(client):
    status = data["bot"]["status"]["status"]
    if streaming == "True":
        platform_ = data["bot"]["status"]["streaming"]["type"]
        name = data["bot"]["status"]["streaming"]["game"]
        url = data["bot"]["status"]["streaming"]["url"]
        await client.change_presence(activity=discord.Streaming(platform=platform_, name=name, url=url))
    elif watching == "True":
        activity = data["bot"]["status"]["watching"]["watching"]
        if status == "online":
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        elif status == "dnd":
            await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        elif status == "idle":
            await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
    elif playing == "True":
        game = data["bot"]["status"]["playing"]["game"]
        if status == "online":
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=game))
        elif status == "dnd":
            await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=game))
        elif status == "idle":
            await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=game))


def download_avatar(url):
    r = requests.get(url)
    if r.status_code != 200:
        return False
    with open('assets/avatar.png', 'wb') as f:
        f.write(r.content)
        return True


def get_price(url):
    try:
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'
        }
        r = requests.get(url, headers=header)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_text = soup.find(
            'div', {'class': 'a-box-group'}).find('span', {'class': 'a-offscreen'}).text
        product_name = soup.find(
            'div', {'id': 'titleSection'}).find('span', {'id': 'productTitle'}).text
        product_image = soup.find(
            'div', {'id': 'main-image-container'}).find('img', {'id': 'landingImage'}).get('src')
        return price_text, product_name, product_image
    except Exception as e:
        print(e)


async def check_exists(name):
    session = aiohttp.ClientSession()
    async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{name}") as response:
        if response.status == 200:
            data = await response.json()
            await session.close()
            return data
        else:
            await session.close()
            return False
