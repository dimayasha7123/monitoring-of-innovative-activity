from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import redis
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
import yaml
import os
import json


with open(os.path.abspath('screenshots/config.yml'), 'r') as file:
    db_settings = yaml.safe_load(file)
    # create ./files if not exists
    if not os.path.exists('./files'):
        os.mkdir('./files')

r = redis.StrictRedis(host=db_settings['host'], port=db_settings['port'], db=db_settings['db'])


def make_screenshot(company_name: str, company_category: str, url: str) -> bool: 
    with webdriver.Firefox() as driver:
        driver.get(url)
        # place = driver.find_element(By.XPATH, f"//*[contains(text(),'{company_name}')]")
        time.sleep(0.5)
        place_png = driver.get_full_page_screenshot_as_png()
        # place_png = place.screenshot_as_png
        filename_json = json.dumps({
            'company_name': company_name,
            'keywords': [company_category.split(", ")],
            'time_stamp': str(datetime.now())
            })
    
    with BytesIO() as output:
        im = Image.open(BytesIO(place_png))
        im.save(output, format='png')
        r.set(filename_json, output.getvalue())
        r.bgsave()

    return True


def get_zip_by_company_name(company_name: str) -> str:
    filenames = [t.decode('utf8') for t in r.keys()]
    filtered_filenames = []
    
    for name in filenames:
        unmarsheld = json.loads(name)
        if unmarsheld['company_name'] == str(company_name):
            filtered_filenames.append(name)


    pipe = r.pipeline()
    
    for name in filtered_filenames:
        pipe.get(name)
    pics = pipe.execute()

    zipname = f'files/{company_name}_{datetime.date(datetime.now())}.zip'
    with ZipFile(zipname, 'w') as tzip:
        for i in range(0, len(pics)):
            tzip.writestr(f'screenshot_{i}.PNG', BytesIO(pics[i]).getvalue())
    return zipname


if __name__ == '__main__':
    company_name = 'МЦЭ-Инжиниринг'
    company_category = 'красавцы'
    url = 'https://mcee.ru/tpost/of551zcy81-20-maya-2021'
    make_screenshot(company_name, company_category, url)
    print(get_zip_by_company_name(company_name)) 


# Code for testing
# ---------------------------------------------------------------

# company_name = 'МЦЭ-Инжиниринг'
# company_category = 'красавцы'
# url = 'https://mcee.ru/tpost/of551zcy81-20-maya-2021'

# make_screenshot(company_name, company_category, url)
# print(get_zip_by_company_name(company_name))

# names = r.keys()
# pic = r.get(names[0])
# im = Image.open(BytesIO(pic))
# im.save(names[0], format='png')

# ---------------------------------------------------------------