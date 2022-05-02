import aiohttp
import requests
from bs4 import BeautifulSoup


def download_avatar(url):
    r = requests.get(url)
    if r.status_code == 200:
        with open('assets/avatar.png', 'wb') as f:
            f.write(r.content)
            return True
    else:
        return False


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
        return price_text, product_name
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