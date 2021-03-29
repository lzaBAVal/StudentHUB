from bs4 import BeautifulSoup
from loader import db

import requests
import datetime

url_arhit = 'https://aues.arhit.kz/rasp/'

def get_all_institutions():

    result = {}
    response = requests.get(url_arhit)
    soup = BeautifulSoup(response.text, 'lxml')
    row = soup.find_all('div', {'class': 'row'})
    time = datetime.datetime.now()
    time = str(time.strftime("%H_%M_%S"))

    old_a: BeautifulSoup = None
    for i in row:
        a = i.find('a', href=True)
        if a and a != old_a:
            sched = None
            action = None
            url = url_arhit + a['href']
            result.setdefault(a.text, [])
            result[a.text].append(str(url))
            old_a = a
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                action = soup.find('form').get('action')
            except Exception:
                pass
            try:
                sched = soup.find('input', {'name': 'schedule'})['value']
            except Exception:
                pass
            if sched:
                sched_url = url_arhit + action + '?sg={value}&schedule=' + sched
            else:
                sched_url = url_arhit + action + '?sg={value}'
            result[a.text].append(str(sched_url))

    try:
        result.pop('Расписание дополнительного семестра')
    except Exception:
        print('Куда то делась запись! SOS!!!')

    result = (str(result))

    with open(time, 'w', encoding="utf-8") as f:
        f.write(result)

    with open(time, 'r', encoding="utf-8") as f:
        institutions = f.read()

    institutions = eval(institutions)
    for i in institutions:
        # asyncio.get_event_loop().run_until_complete(pgsql_conn(add_institution(i, institutions[i][0], institutions[
        # i][1])))
        db.add_institution(i, institutions[i][0], institutions[i][1])