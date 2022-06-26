from requests import get
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import cfscrape
from parsing.analyze import get_orgs_from_text, classify
import dateparser
import re
import datetime
from project.models import Company, TableAnalyzeCompany

def get_site_info(url):
    name = urlparse(url).hostname
    for s in sites['sites']:
        if urlparse(s['URL']).hostname == name:
            return s
    return {"URL": None}

def str_to_date(text):
    for i in range(len(text)):
        if text[i].isdigit():
            break
    d = dateparser.parse(text[i:])
    return d.strftime("%Y-%m-%d")

def find_org(orgs):
    all_orgs = Company.objects.all().values_list('cat_id', 'other_name')
    # print(all_orgs)
    our_orgs = []
    for s in orgs:
        for c in all_orgs:
            if c[1] and s in c[1]:
                our_orgs.append(c[0])
    return list(set(our_orgs))


def parse_and_save(url, keywords=None):
    code, result = parse(url, keywords)
    # print(result)
    if code:
        orgs = find_org(result["org"])
        for org in orgs:
            p = TableAnalyzeCompany()
            p.company_name = Company.objects.get(cat_id=org)
            p.url = result["URL"]
            p.name_news =  result["name"]
            p.name_title_news = result["title"]
            p.date_news =  result["date"]
            p.category = ", ".join(result["keywords"])
            p.save()
    else:
        print(result)
    return code
       

def parse(url, keywords=None):
    if not keywords:
        keywords = ["технологии", "импортозамещение", "инновации",
                    "научные разработки", "патенты",
                    "гранты", "исследования"]
    try:
        scraper = cfscrape.create_scraper(delay=5)
        response = scraper.get(url) #,  headers={"useragent": f"{ua.random}"})

        if response:
            soup = BeautifulSoup(response.text, "lxml")
            site_info = get_site_info(url)
            if site_info["URL"]:
                #title = soup.find(class_=site_info["title"]).text
                title = soup.select_one(site_info["title"]).text
                title = title.replace('\n', " ").replace('\t', " ").strip()
                date = soup.select_one(site_info["date"]).text
                date = date.replace('\n', " ").replace('\t', " ").strip()
                date = str_to_date(date)
                text = soup.select_one(site_info["text"]).get_text()
                text = text.replace('\n', " ").replace('\t', " ").strip()
                classes = classify(text, keywords)
                orgs = get_orgs_from_text(text)
                return 1, \
                       {"org": orgs,
                        "name": urlparse(url).hostname,
                        "title": title,
                        "date": date,
                        "URL": url,
                        "text": text,
                        "keywords": classes
                }
            else:
                title = soup.find("h1")
                if not title:
                    title = soup.find(class_=re.compile("title"))
                if not title:
                    title = soup.find(class_=re.compile("header"))
                if not title:
                    title = soup.find(class_=re.compile("intro"))
                if not title:
                    title = ""
                else:
                    title = title.text.replace('\n', " ").replace('\t', " ").strip()
                date = soup.find(class_=re.compile("date"))
                if date:
                    date = date.text.replace('\n', " ").replace('\t', " ").strip()
                else:
                    date = "today"
                date = str_to_date(date)
                text = soup.find(class_=re.compile("detail"))
                if not text:
                    text = soup.find(class_=re.compile("content"))
                if not text:
                    text = soup.find(class_=re.compile("text"))
                if not text:
                    text = soup
                text = text.get_text()
                text = text.replace('\n', " ").replace('\t', " ").strip()
                classes = classify(text, keywords)
                orgs = get_orgs_from_text(text)
                return 1, \
                       {"org": orgs,
                        "name": urlparse(url).hostname,
                        "title": title,
                        "date": date,
                        "URL": url,
                        "text": text,
                        "keywords": classes
                }
        else:
            return 0, {"Error_code": response.status_code}
    except Exception as err:
        return 0, {"Error": str(err)}


try:
    sites = json.load(open('static/sites.json', encoding='utf-8'))
except:
    sites = {
        "sites": [
                    ]
    }
