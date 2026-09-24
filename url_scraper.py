from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def scrape_urls():
    url = "https://www.gamedevmap.com/index.php?location=&country=Canada&state=Ontario&city=&query=&type=&start=61&count=227"

    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")

    data = []

    for a in soup.select("tr td b a"):
        name = a.get_text(strip=True)
        href = a.get("href")
        if href is None:
            continue
        link = urljoin(url, str(href))
        data.append((name, link))

    for name, link in data:
        print(name, link, sep=",")


scrape_urls()
