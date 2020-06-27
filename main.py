'''
@author: Dipin Arora
'''
import requests
from bs4 import BeautifulSoup as bs
import time
import asyncio
import aiohttp
import csv
import sys

DOMAIN_ZONE = 'com'
links = []


async def scrape(session, page_num):
    async with session.get(
            f'https://onshopify.com/domain-zone/{DOMAIN_ZONE}/{page_num}'
    ) as res:
        if res.status == 200:
            text = await res.text()
            soup = bs(text, features='html.parser')
            for link in soup.find_all(
                    attrs={'class': 'col-lg-4 col-md-4 col-sm-12'}):
                if link.text.strip().endswith(f'.{DOMAIN_ZONE}'):
                    links.append(link.text.strip())


async def fetch(last_page):
    async with aiohttp.ClientSession() as session:
        tasks = []
        print(f'Scraping till page number {last_page}')
        for page_num in range(1, last_page):
            task = asyncio.ensure_future(scrape(session, page_num))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


def last_page_finder():
    res = requests.get(f'https://onshopify.com/domain-zone/{DOMAIN_ZONE}/')
    if res.status_code == 200:
        soup = bs(res.text, features='html.parser')
        x = soup.find(attrs={'class': 'pagination'})
        if x is not None:
            return int(x.find_all('li').pop().text)
        else:
            raise Exception(
                'Invalid Domain Zone\nYou can find valid domain at https://onshopify.com/domains'
            )


if __name__ == "__main__":
    t = time.time()
    if len(sys.argv) > 1:
        DOMAIN_ZONE = sys.argv[1]
    print('scraping started')
    if len(sys.argv) > 2:
        last_page = int(sys.argv[2])
        if last_page < 0:
            raise Exception('Last Page cannot be less than 0')
    else:
        last_page = last_page_finder()
    asyncio.get_event_loop().run_until_complete(fetch(last_page))
    f = open('script_output.csv', 'w', newline='')
    fil = csv.writer(f)
    for link in links:
        fil.writerow([link])
    print(time.time() - t)
