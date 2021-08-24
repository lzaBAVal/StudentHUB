import re
from datetime import datetime

from DB.models import Group, Student, Subject
from DB.models.db import db
from bot.schedule.output.get_schedule_object import decode_normalise_sched
from bot.vars import Sched
from config.db import load_db_config
from log.logging_core import init_logger

all_lessons = []
logger = init_logger()


async def add_object_for_group(message):
    group_id = await Student.filter(chat_id=message.chat.id).values_list('group_id')
    group_id = group_id[0][0]
    lessons = await harvest_subject(group_id)
    if lessons == -1:
        return 1
    await add_subject(lessons, message)


async def init():
    core_db = load_db_config()
    await db.db_init(core_db)


async def get_sched_obj(group_id):
    sched = await Group.filter(id=group_id).values_list('sched_arhit')
    sched = sched[0][0]
    sched = decode_normalise_sched(sched)
    if sched == -1:
        return 1
    sched = Sched.parse_obj(sched)
    return sched


# Harvest one task_subject
async def harvest_subject(group_id):
    try:
        sched: Sched = await get_sched_obj(group_id)
        if sched == -1:
            return 1
    except Exception:

        print(f"group with id: {group_id} have not sched")
        pass
    else:
        for day in sched:
            if not (day[1] is None):
                for lessons in day[1]:
                    for lesson in lessons[1]:
                        lesson = parse_subject(lesson.lesson)
                        lesson = lesson[0]
                        if not (lesson in all_lessons):
                            all_lessons.append(lesson)
        return all_lessons


async def add_subject(lessons, message):
    for i in range(len(lessons)):
        student_info = await Student.filter(chat_id=message.chat.id).values_list('id', 'group_id')
        student_info = student_info[0]
        await Subject(name=lessons[i],
                      user_id=student_info[0],
                      group_id=student_info[1],
                      date_creation=datetime.now().strftime('%Y-%m-%d')).save()


async def delete_subject(message, subject_name):
    student_info = await Student.filter(chat_id=message.chat.id).values_list('id', 'group_id')
    student_info = student_info[0]
    await Subject.filter(user_id=student_info[0], group_id=student_info[1], name=subject_name).delete()


def parse_subject(lesson: str):
    all_parts = re.findall(r'(.*)[ ]{1,3}(лаб\.|лек\.|прак\.)(.*)', lesson)
    all_parts = all_parts[0]

    if all_parts[2] == '':
        all_parts = all_parts[:2]
    if len(all_parts) != 2:
        unparsed_subject(all_parts)
    else:
        return all_parts


def unparsed_subject(parts):
    with open('unparsed.txt', 'a') as file:
        file.write(str(str(parts).encode('utf-8')) + '\n')

    '''
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(coro)
        finally:
            loop.run_until_complete(Tortoise.close_connections())
    '''
