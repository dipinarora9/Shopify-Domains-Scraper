'''
@author: Dipin Arora
'''
import requests
from bs4 import BeautifulSoup as bs
import time
import asyncio
import aiohttp
import csv

TILL_PAGE_NUM = 7424
links = []


async def scrape(session, page_num):
    async with session.get(
            f'https://onshopify.com/domain-zone/com/{page_num}') as res:
        if res.status == 200:
            text = await res.text()
            soup = bs(text, features='html.parser')
            for link in soup.find_all(
                    attrs={'class': 'col-lg-4 col-md-4 col-sm-12'}):
                if link.text.strip().endswith('.com'):
                    links.append(link.text.strip())


async def fetch():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_num in range(1, TILL_PAGE_NUM):
            task = asyncio.ensure_future(scrape(session, page_num))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    t = time.time()
    asyncio.get_event_loop().run_until_complete(fetch())
    f = open('a.csv', 'w', newline='')
    fil = csv.writer(f)
    for link in links:
        fil.writerow([link])
    print(time.time() - t)
