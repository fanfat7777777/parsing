from selenium import webdriver
from selenium.webdriver.common.by import By         # Для поиска
from selenium.webdriver.firefox.service import Service  # Драйвер брайзера
from selenium.webdriver.common.keys import Keys     # Обработка действий кнопок
# Для обработки появляющихся модулей через время
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pymongo import MongoClient
from pprint import pprint

# БД
client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
db_products = db.products

s = Service('./geckodriver.exe')
driver = webdriver.Firefox(service=s)

driver.get('https://www.mvideo.ru/')


# Прокрутка
scrolling = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.TAG_NAME, 'body'))
)
scrolling.send_keys(Keys.PAGE_DOWN)
sleep(2)
scrolling.send_keys(Keys.PAGE_DOWN)


# Кликаем на тренды
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, '//mvid-shelf-group//button[2]'))
).click()

count = 1
while True:
    item = {}
    try:
        name = driver.find_element(By.XPATH, f"//mvid-shelf-group//*[contains(@class, 'card__name')][{count}]").text
        item['Название'] = name
        price = driver.find_element(By.XPATH, f"//mvid-shelf-group//*[contains(@class, 'card__price')][{count}]//*[contains(@class, '__main')]").text
        item['Цена'] = price
        href = driver.find_element(By.XPATH, f"//mvid-shelf-group//*[contains(@class, 'card__name')][{count}]//a").get_attribute('href')
        item['Ссылка'] = href
        db_products.insert_one(item)
    except:
        print('except')
        break

    count += 1

for item in db_products.find({}):
    pprint(item)
