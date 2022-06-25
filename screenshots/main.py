from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import redis
from PIL import Image
from io import BytesIO


company_name = 'МЦЭ-Инжиниринг'
company_category = 'красавцы'
url = 'https://mcee.ru/tpost/of551zcy81-20-maya-2021'

r = redis.StrictRedis(host='localhost', port='6379', db=0)

def make_screenshot(company_name: str, company_category: str, url: str) -> bool: 
    with webdriver.Firefox() as driver:
        driver.get(url)
        place = driver.find_element(By.XPATH, f"//*[contains(text(),'{company_name}')]")
        time.sleep(0.5)
        place_png = place.screenshot_as_png
        filename = f'./{company_name}_{company_category}_{datetime.now()}.PNG'
    
    with BytesIO() as output:
        im = Image.open(BytesIO(place_png))
        im.save(output, format='png')
        r.set(filename, output.getvalue())
        r.bgsave()

    return True

# Code for testing

make_screenshot(company_name, company_category, url)
names = r.keys()
pic = r.get(names[0])
im = Image.open(BytesIO(pic))
im.save(names[0], format='png')
