import os
import requests
from bs4 import BeautifulSoup
import fake_useragent
import urllib3
import logging
import datetime
import pytz

SERVICE = "moodle_mobile_app"
username = "dzhygst315"
password = "56517833"
session = requests.Session()
user = fake_useragent.FakeUserAgent()
link = f'https://elr.tnpu.edu.ua/login/index.php'
headers = {'User-Agent': user.random}

# Отримуємо logintoken
response = session.post(link)
print(response.text)
