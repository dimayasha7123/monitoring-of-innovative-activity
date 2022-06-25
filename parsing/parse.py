from requests import get
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import cloudscraper
import cfscrape
#from fake_useragent import UserAgent



def get_site_info(url):
    name = urlparse(url).hostname
    for s in sites['sites']:
        if urlparse(s['URL']).hostname == name:
            return s
    return {"URL": None}


def parse(url):
    try:
        # scraper = cloudscraper.create_scraper()
        """
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        """

 #       ua = UserAgent()
        scraper = cfscrape.create_scraper(delay=5)
        response = scraper.get(url) #,  headers={"useragent": f"{ua.random}"})

        if response:
            soup = BeautifulSoup(response.text, "lxml")
            site_info = get_site_info(url)
            if site_info["URL"]:
                title = soup.find(class_=site_info["title"]).text
                title = title.replace('\n', " ").replace('\t', " ")
                date = soup.find(class_=site_info["date"]).text.replace('\n', " ")
                date = date.replace('\n', " ").replace('\t', " ")
                text = soup.find(class_=site_info["text"]).text.replace('\n', " ")
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
            {
                "URL": "https://orenburzhie.ru/",
                "news": "https://orenburzhie.ru/category/news/",
                "title": "entry-title",
                "date": "entry-date",
                "text": "entry-content"
            },
            {
                "URL": "https://orenburg.media/",
                "news": "https://orenburg.media/?cat=3",
                "title": "post-title",
                "date": "post-byline",
                "text": "post-content"
            },
            {
                "URL": "https://orennc.ru/",
                "news": "https://orennc.ru/?page_id=30",
                "title": "tg-page-header__title",
                "date": "entry-date published",
                "text": "entry-content"
            }]
    }
