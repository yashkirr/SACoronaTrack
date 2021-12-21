"""
Author: Yashkir Ramsamy
Contact: me@yashkir.co.za
Date: 2020/07/13

Purpose: Parse Stats from worldometers.info
"""

import requests
import hashlib
from bs4 import BeautifulSoup

DATA_SOURCE = "https://www.worldometers.info/coronavirus/country/south-africa/"
stats = []  # in case there's a need to implement more


def parse():
    print("PARSING: Getting web content")
    web_page = requests.get(DATA_SOURCE).content
    soup = BeautifulSoup(web_page, "html.parser")
    print("PARSING: Parsing web content")
    for div in soup.find_all('div', class_='maincounter-number'):
        stat = div.span.text
        stats.append(int(stat.replace(',', '')))

def getHash():
    web_page = requests.get(DATA_SOURCE)
    return hashlib.sha256(web_page.text.encode("utf-8")).hexdigest()

# returns list where:
#   [0]: Cases
#   [1]: Deaths
#   [2]: Recoveries
def getNationalStats():
    parse()
    return stats


if __name__ == "__main__":
    print(getNationalStats())

