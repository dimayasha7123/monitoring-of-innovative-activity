from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import redis


company_name = 'МЦЭ-Инжиниринг'
url = 'https://mcee.ru/tpost/of551zcy81-20-maya-2021'


def make_screenshot(company_name: str, url: str) -> bool: 
    with webdriver.Firefox() as driver:
        driver.get(url)
        place = driver.find_element(By.XPATH, f"//*[contains(text(),'{company_name}')]")
        time.sleep(0.5)
        place.screenshot(f'./{company_name}_{datetime.now()}.png')
    return True

make_screenshot(company_name, url)

#screenshot(f'./{company_name}_{datetime.now()}.png')