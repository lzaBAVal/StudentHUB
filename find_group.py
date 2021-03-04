'''

    Функция group_search принимает строковое значение (наименование группы) и отдает id_inc БД в случае
     точного нахождения группы, в случае если найдено несколько групп, отдает списки

'''

import re
from loader import db

'''
def search_shed_using_group(require_group: str):
    require_group = require_group.lower().strip()
    url = 'https://aues.arhit.kz/rasp/start3.php'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    groups_dict = {}
    group_list = []
    matched_group_list = []
    result = None

    for opt in soup.find_all('option'):
        groups_dict.setdefault(str(opt.string).lower().strip(), opt['value'])

    groups_dict.pop('- группа -')

    for i in groups_dict.keys():
        group_list.append(re.findall(r'([a-zA-zа-яА-Я\(\)\-\w]{1,10})\-(\d{2})\-(\d{1,2})', i))

    req_g_list = re.findall(r'([a-zA-zа-яА-Я\(\)\-\w]{1,10})[\-|" *"]+(\d{2})[\-|" *"]+(\d{1,2})', require_group)

    branch_mame = str(re.findall(r'^[а-я А-Я]{2}', require_group)[0])

    for item_g in group_list:
        if item_g != []:
            counter = 0
            for i in range(3):
                if re.search(rf"{branch_mame}", item_g[0][0]):
                    if i == 0 and str(req_g_list[0][i]) == item_g[0][i].replace('(','').replace(')', ''):
                        counter += 1
                    else:
                        if (req_g_list[0][i] == item_g[0][i]):
                            counter += 1
                else:
                    break

            if counter == 2:
                matched_group_list.append(item_g)
            if counter == 3:
                result = str("-".join(item_g[0][:]))
                break
    if result != None:
        group = str(groups_dict[result.lower()])
        result = requests.get("https://aues.arhit.kz/rasp/scheduleNew.php?sg={0}&schedule=32".format(group))
        return str(result)
    else:
        return list(matched_group_list)
'''

'''
    for opt in soup.find_all('option'):
        groups_dict.setdefault(str(opt.string).lower().strip(), opt['value'])

    groups_dict.pop('- группа -')

    for i in groups_dict.keys():
        group_list.append(re.findall(r'([a-zA-zа-яА-Я\(\)\-\w]{1,10})\-(\d{2})\-(\d{1,2})', i))

    req_g_list = re.findall(r'([a-zA-zа-яА-Я\(\)\-\w]{1,10})[\-|" *"]+(\d{2})[\-|" *"]+(\d{1,2})', require_group)

    branch_mame = str(re.findall(r'^[а-я А-Я]{2}', require_group)[0])

    for item_g in group_list:
        if item_g != []:
            counter = 0
            for i in range(3):
                if re.search(rf"{branch_mame}", item_g[0][0]):
                    if i == 0 and str(req_g_list[0][i]) == item_g[0][i].replace('(','').replace(')', ''):
                        counter += 1
                    else:
                        if (req_g_list[0][i] == item_g[0][i]):
                            counter += 1
                else:
                    break

            if counter == 2:
                matched_group_list.append(item_g)
            if counter == 3:
                result = str("-".join(item_g[0][:]))
                break
    if result != None:
        group = str(groups_dict[result.lower()])
        result = requests.get("https://aues.arhit.kz/rasp/scheduleNew.php?sg={0}&schedule=32".format(group))
        return str(result)
    else:
        return list(matched_group_list)
        
'''


async def group_search(group: str):
    comp_match, match, other_match = [], [], []
    req_g_list = list(re.findall(r'([a-z а-я \(\)\-\w]{1,10})[\-|" *"]+(\d{2})[\-|" *"]+(\d{1,2})', group.lower())[0])
    branch_mame = "".join(re.findall(r'^[а-я А-Я a-z A-Z]{2}', group))
    response = await db.get_all_groups()
    for i in response:
        name = dict(i)['group_name']
        if re.search(rf"{req_g_list[1]}", name) and re.search(rf"{req_g_list[2]}", name):
            if re.search(rf"{req_g_list[0]}", name):
                comp_match.append(name)
            elif re.search(rf"{branch_mame}", name):
                match.append(name)
            else:
                other_match.append(name)

    return comp_match, match, other_match