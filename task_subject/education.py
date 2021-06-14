import json

from aiogram import types
from models import Student, Subject, Task, Photo, Document

chat_id = 690976128


# TODO CONFIGURE LAST
async def get_academic_tasks(message: types.Message):
    group_id = await Student.filter(chat_id=message.chat.id).values_list('group_id')
    group_id = group_id[0][0]
    subjects = await Subject.filter(group_id=group_id).values('id', 'name')
    all_tasks = {}
    for i in subjects:
        name_task = await Task.filter(subject_id=i['id']).values_list('name', 'id')
        if name_task:
            for task in name_task:
                task_name_id = {task[0]: task[1]}
                if i['name'] in all_tasks:
                    all_tasks[i['name']].append(task_name_id)
                else:
                    all_tasks.setdefault(i['name'], []).append(task_name_id)
    return all_tasks


async def get_subjects(message: types.Message):
    group_id = await Student.filter(chat_id=message.chat.id).values_list('group_id')
    group_id = group_id[0][0]
    subjects = await Subject.filter(group_id=group_id).values_list('name')
    all_subjects = []
    for subject in subjects:
        all_subjects.append(subject[0])
    return all_subjects


def exclude_variant(excluded: str):
    variants = excluded.split()
    variant_dict = {}
    for variant in variants:
        variant_dict[variant] = 'excluded'
    return json.dumps(variant_dict)


async def check_existed_task(name, subject_id):
    task = await Task.filter(name=name, subject_id=subject_id)
    if task:
        return 1
    else:
        return 0


async def get_task_info(task_id):
    task_info = await Task.filter(id=task_id).values_list('name', 'description', 'user_variant')
    task_info = task_info[0]

    message = f'Название таска: {task_info[0]}\n' \
              f'Описание: {task_info[1]}\n' \
              f'Доступные варианты работ: {task_info[2]}'

    photos = await Photo.filter(task_id=task_id).values_list('telegram_id')
    documents = await Document.filter(task_id=task_id).values_list('telegram_id')
    return message, photos, documents


async def deleteSubject(message: types.Message, task_subject):
    result = await Student.filter(chat_id=chat_id).prefetch_related('user_id')
    for i in result:
        for j in i.user_id:
            if j.name == task_subject:
                await Subject.filter(id=j.id).delete()
    await Subject.filter()
    return 0
