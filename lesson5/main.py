# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о
# письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError
import time
s = Service('./chromedriver')
driver = webdriver.Chrome()

driver.get('https://account.mail.ru/login/?mode=simple&v=2.8.2&account_host=account.mail.ru&type=login&modal=1&allow_external=1&success_redirect=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox%3Fback%3D1&opener=mail.login&noinnerscroll=1&wide=1&rebranding2018=1&parent_url=https%3A%2F%2Fe.mail.ru%2Flogin')
driver.implicitly_wait(5)

elem = driver.find_element(By.NAME, 'username')
elem.send_keys("study.ai_172")
elem.send_keys(Keys.ENTER)
driver.implicitly_wait(1)
#elem_b = driver.find_element(By.XPATH, '//div[@class="submit-button-wrap"]/button[@data-test-id="next-button"]"'
elem = driver.find_element(By.NAME, 'password')
elem.send_keys("NextPassword172#")
elem.send_keys(Keys.ENTER)

driver.implicitly_wait(10)

elem_m = driver.find_elements(By.XPATH, "//div[contains(@class, 'ReactVirtualized__Grid')]//a")
body = driver.find_elements(By.XPATH,'//body')
pprint(body[0])

message_list = []
st_p = 0
for n in range(0,2):
    for el in elem_m:
        message_info = {}
        message_id = el.get_attribute("data-id")
        message_href = el.get_attribute("href")
        message_info['_id'] = message_id
        message_info['href'] = message_href
        message_list.append(message_info)
        # здесь нужно заходить в каждое отдельно письмо, открывать и смотреть отправителя, дату, время
        # на общей странчке на mail нет идентификаторов, с помощью которых возможно было бы прописать xpath или найти по атрибуту
        # оставлю эту задачу "за скобками"
    driver.implicitly_wait(5)
    driver.execute_script("window.scrollTo(" + str(st_p) + ", " + str(st_p+1800) +");") #не прокручивает :(
    body[0].send_keys(Keys.PAGE_DOWN) #тоже не прокручивает :(
    st_p = st_p + 1800
    time.sleep(1)
    driver.implicitly_wait(5)

#pprint(message_list)
pprint(len(message_list))

client = MongoClient('127.0.0.1', 27017)
db = client['db_messages']
mes = db.mes

def add_mess(th_mes):
    try:
        mes.insert_one(th_mes)
        print('added')
    except DuplicateKeyError:
        print('Message is already exist')


for message in message_list:
    add_mess(message)

