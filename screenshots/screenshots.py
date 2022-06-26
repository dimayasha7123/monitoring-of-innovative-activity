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


with open(os.path.abspath('screenshots/config.yml'), 'r') as file:
    db_settings = yaml.safe_load(file)

r = redis.StrictRedis(host=db_settings['host'], port=db_settings['port'], db=db_settings['db'])


def make_screenshot(company_name: str, company_category: str, url: str) -> bool: 
    with webdriver.Firefox() as driver:
        driver.get(url)
        # place = driver.find_element(By.XPATH, f"//*[contains(text(),'{company_name}')]")
        time.sleep(0.5)
        place_png = driver.get_full_page_screenshot_as_png()
        # place_png = place.screenshot_as_png
        filename = f'{company_name}_{company_category}_{datetime.now()}.PNG'
    
    with BytesIO() as output:
        im = Image.open(BytesIO(place_png))
        im.save(output, format='png')
        r.set(filename, output.getvalue())
        r.bgsave()

    return True


def get_zip_by_company_name(company_name: str) -> str:
    filenames = [t.decode('utf8') for t in r.keys()]
    filtered_filenames = []
    
    for name in filenames:
        if name.split('_')[0] == company_name:
            filtered_filenames.append(name)

    pipe = r.pipeline()
    
    for name in filtered_filenames:
        if name != '': pipe.get(name)
    pics = pipe.execute()

    zipname = f'files/{company_name}_{datetime.date(datetime.now())}.zip'
    with ZipFile(zipname, 'w') as tzip:
        for i in range(0, len(pics)):
            tzip.writestr(filtered_filenames[i], BytesIO(pics[i]).getvalue())
    return zipname


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