from requests import get
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import cloudscraper
import cfscrape



def get_site_info(url):
    name = urlparse(url).hostname
    for s in sites['sites']:
        if urlparse(s['URL']).hostname == name:
            return s
    return {"URL": None}


def parse(url):
    try:
        scraper = cfscrape.create_scraper(delay=5)
        response = scraper.get(url) #,  headers={"useragent": f"{ua.random}"})

        if response:
            soup = BeautifulSoup(response.text, "lxml")
            site_info = get_site_info(url)
            if site_info["URL"]:
                #title = soup.find(class_=site_info["title"]).text
                title = soup.select_one(site_info["title"]).text
                title = title.replace('\n', " ").replace('\t', " ")
                date = soup.select_one(site_info["date"]).text
                date = date.replace('\n', " ").replace('\t', " ")
                text = soup.select_one(site_info["text"]).text
                text = text.replace('\n', " ").replace('\t', " ")
                return 1, {"URL": url, "title": title, "date": date,
                        "text": text}
            else:
                return 0, {"Error": "site is unknown"}  # TODO Universal Parser
        else:
            return 0, {"Error_code": response.status_code}
    except Exception as err:
        return 0, {"Error": str(err)}


try:
    sites = json.load(open('../static/sites.json', encoding='utf-8'))
except:
    sites = {
        "sites": [
                    ]
    }
