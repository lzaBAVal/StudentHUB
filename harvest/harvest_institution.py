from bs4 import BeautifulSoup
from DB.pgsql_conn import pgsql_conn
from DB.pgsql_requests import insert_institution

import requests
import datetime
import asyncio

url_arhit = 'https://aues.arhit.kz/rasp/'

def get_all_institutions():

    result = {}
    responce = requests.get(url_arhit)
    soup = BeautifulSoup(responce.text, 'lxml')
    soup = soup.find_all('div', {'class': 'row'})
    time = datetime.datetime.now()
    time = time.strftime("%H_%M_%S")

    old_a: BeautifulSoup = None
    for i in soup:
        a = i.find('a', href=True)
        if a and a != old_a:
            url = url_arhit + a['href']
            result.setdefault(a.text, [])
            result[a.text].append(str(url))
            old_a = a

    result = (str(result))
    print(result)
    with open(str(time), 'w', encoding="utf-8") as f:
        f.write(result)


def fill_institutions():
    with open('reference.txt', 'r', encoding="utf-8") as f:
        institutions = f.read()

    institutions = eval(institutions)

    for i in institutions:
        asyncio.get_event_loop().run_until_complete(pgsql_conn(insert_institution(i, institutions[i][0], institutions[i][1])))
