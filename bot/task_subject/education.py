import json

from aiogram import types

from DB.models import Student, Subject, Task, Photo, Document
from DB.models.student import get_all_students_name_id, get_student_id


async def get_all_tasks(message: types.Message):
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
    print(excluded)
    if not excluded:
        return json.dumps({})
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
    range_variants = await get_range_variants(task_id)
    message = f'Название таска: {task_info[0]}\n' \
              f'Описание: {task_info[1]}\n' \
              f'Диапазон вариантов работ: {range_variants[0]}-{range_variants[1]}'

    photos = await Photo.filter(task_id=task_id).values_list('telegram_id')
    documents = await Document.filter(task_id=task_id).values_list('telegram_id')
    return message, photos, documents


async def deleteSubject(message: types.Message, task_subject):
    result = await Student.filter(chat_id=message.chat.id).prefetch_related('user_id_for_subject')
    for j in result[0].user_id_for_subject:
        if j.name == task_subject:
            await Subject.filter(id=j.id).delete()
    await Subject.filter()
    return 0


async def get_tasks_of_subject(message: types.Message, subject: str) -> dict:
    group_id = await Student.filter(chat_id=message.chat.id).values_list('group_id')
    group_id = group_id[0][0]
    subjects = await Subject.filter(group_id=group_id, name=subject).values('id', 'name')
    all_tasks = {}
    for i in subjects:
        name_task = await Task.filter(subject_id=i['id']).values_list('name', 'id')
        if name_task:
            for name, task_id in name_task:
                all_tasks.update({name: task_id})
    return all_tasks


async def get_taken_variants(task_id) -> dict:
    variants = await Task.filter(id=task_id).values_list('user_variant')
    variants = variants[0][0]
    return variants


async def get_variants_and_users(task_id, msg: types.Message) -> dict:
    variants = await Task.filter(id=task_id).values_list('user_variant')
    variants = variants[0][0]
    if variants is None:
        return 'У данной работы нет вариантов'
    students = await get_all_students_name_id(msg)
    result = ''
    for key in variants:
        if variants[key] != "excluded":
            value = variants[key]
            if str(value).isdigit():
                if int(value) in list(students.keys()):
                    result += f"\n{int(key)} - {students[int(value)]}"
    return result


async def check_available_variant(all_variants: dict = None, variant=None,
                                  task_id: int = None, msg: types.Message = None):
    range_variants = await Task.filter(id=task_id).values_list('variant_start', 'variant_end')
    range_variants = range_variants[0][:]
    if variant < range_variants[0] or variant > range_variants[1]:
        return False
    taken = all_variants.get(str(variant))
    if taken is None:
        return True
    else:
        return False


async def check_taken_yet_variant(msg: types.Message, variants: dict):
    stud_id = await get_student_id(msg)
    print(f'check_taken_yet_variant: {stud_id}')
    if stud_id in list(variants.values()):
        print(f'check_taken_yet_variant TRUE: {stud_id}')
        return True
    else:
        return False


async def add_variant(task_id=None, msg: types.Message = None):
    variants = await Task.filter(id=task_id).values_list('user_variant')
    variants: dict = variants[0][0]
    student_id = await Student.filter(chat_id=msg.chat.id).values_list('id')
    variants.update({msg.text: student_id[0][0]})
    await Task.filter(id=task_id).update(user_variant=json.dumps(variants))


async def check_busy_variant(task_id, msg):
    variants = await Task.filter(id=task_id).values_list('user_variant')
    variants: dict = variants[0][0]
    student_id = await Student.filter(chat_id=msg.chat.id).values_list('id')
    student_id = student_id[0][0]
    var = list(variants.values())
    if student_id in var:
        return True
    return False


async def release_variant(task_id, msg: types.Message):
    variants = await Task.filter(id=task_id).values_list('user_variant')
    variants: dict = variants[0][0]
    student_id = await Student.filter(chat_id=msg.chat.id).values_list('id')
    student_id = student_id[0][0]
    print(variants)
    variants_copy = variants.copy()
    for k, v in variants_copy.items():
        if v == student_id:
            variants.pop(k)
            print(f'result: {variants}')
    await Task.filter(id=task_id).update(user_variant=json.dumps(variants))


async def get_range_variants(task_id):
    range_variants = await Task.filter(id=task_id).values_list('variant_start', 'variant_end')
    range_variants = range_variants[0][:]
    return range_variants
