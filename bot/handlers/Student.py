import datetime
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile

from DB.models import Group, Student, Photo
from bot.functions.command import delete_user
from bot.functions.other.calculator import calc_basic
from bot.functions.student.change_schedule import check_privilege_whose
from bot.functions.student.get_schedule import get_all_schedule, get_todays_shedule, get_next_lesson, \
    get_tommorow_lesson, \
    get_output_free_time
from bot.functions.student.other import get_list_of_classmates, get_bio
from bot.keyboard.keyboard import configuration_kb, change_sched_kb, days, stud_kb, other_kb, \
    configure_schedule_kb, manage_task_kb, createButtons, task_menu_kb, question_kb
from bot.states.states import StudentStates, AddLesson, DeleteLesson, DiscoverFreeTime, SetCaptainState, \
    Calculate, Subjects, TakeVariant, TakeAwayVariant
from bot.strings.commands import *
from bot.strings.messages import *
from bot.task_subject.education import get_subjects, get_tasks_of_subject, get_taken_variants, get_task_info, \
    check_available_variant, add_variant, get_variants_and_users, release_variant, check_taken_yet_variant, \
    get_range_variants, check_busy_variant
from config.main import load_config
from log.logging_core import init_logger
from misc import dp
from old_config import PATH_WIN

logger = init_logger()
current_config = load_config()
app_dir: Path = Path(__file__)

db = current_config.db


# BACK TO MENU
@dp.message_handler(Text(equals=back_to_menu_str, ignore_case=True), state=StudentStates.student)
async def back_to_menu(message: types.Message, state: FSMContext):
    privilege = (await state.get_data())['captain_middleware']
    await message.answer('Вы в главном меню', reply_markup=await stud_kb(state))


# MENU OTHER
@dp.message_handler(Text(equals=other_str, ignore_case=True), state=StudentStates.student)
async def menu_other(message: types.Message):
    await message.answer(text=f'Панель "{other_str}"', reply_markup=other_kb)


# MENU CONFIGURE SCHEDULE
@dp.message_handler(Text(equals=configure_schedule_str, ignore_case=True), state=StudentStates.student)
async def menu_configure_schedule(message: types.Message):
    await message.answer(text=f'Панель "{configure_schedule_str}"', reply_markup=configure_schedule_kb)


# MENU MANAGE TASKS
@dp.message_handler(Text(equals=academic_task_str, ignore_case=True), state=StudentStates.student)
async def menu_academic_task(message: types.Message):
    await message.answer(text=f'Меню "{academic_task_str}"', reply_markup=manage_task_kb)


# GET PHOTO
@dp.message_handler(Text(equals='cat', ignore_case=True), state=StudentStates.student)
async def get_photo(message: types.Message):
    hash = await Photo.all().first().values_list('file_id')
    hash = str(hash[0][0])
    await message.answer_photo(InputFile(Path(f"{PATH_WIN}\{hash[:2]}\{hash[:4]}\{hash}.jpg")))
    # await message.answer_photo(InputFile(Path('FS/tmp/tmp_files.jpg')))


# GET ALL SCHEDULE
@dp.message_handler(Text(equals=all_schedule_str, ignore_case=True), state=StudentStates.student)
async def all_shedule_student(message: types.Message):
    await get_all_schedule(message)


# GET TODAYS LESSONS
@dp.message_handler(Text(equals=todays_shedule_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def todays_shedule(message: types.Message):
    await get_todays_shedule(message)


# GET NEXT LESSON
@dp.message_handler(Text(equals=next_lesson_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def next_lesson(message: types.Message):
    await get_next_lesson(message)


# GET TOMMOROW LESSON
@dp.message_handler(Text(equals=tommorow_shedule_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def tommorow_lesson(message: types.Message):
    await get_tommorow_lesson(message)


# CHANGE CONFIGURATION
@dp.message_handler(Text(equals=configuration_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def change_sched(message: types.message):
    await message.answer('Что вы хотите изменить в настройках?', reply_markup=configuration_kb)


# CHANGE SCHEDULE
@dp.message_handler(Text(equals=change_sched_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def change_sched(message: types.message):
    await message.answer('Что вы хотите сделать с расписанием?', reply_markup=change_sched_kb)


# ADD LESSON INITIAL
@dp.message_handler(Text(equals=add_lesson_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def add_lesson_start(message: types.message, state: FSMContext):
    if (await check_privilege_whose(message, state)) == 0:
        await message.answer('В какой день вы хотите добавить урок?', reply_markup=days())
        await AddLesson.time.set()


# DELETE LESSON INITIAL
@dp.message_handler(Text(equals=delete_lesson_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def add_lesson_process_yes(message: types.message, state: FSMContext):
    if (await check_privilege_whose(message, state)) == 0:
        await message.answer('Выберите день:', reply_markup=days())
        await DeleteLesson.lesson.set()


# GET FREE TIME OF DAY 1
@dp.message_handler(Text(equals=discover_free_time_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def discover_free_time(message: types.message):
    await message.answer('Выберите день:', reply_markup=days())
    await DiscoverFreeTime.output.set()


# GET FREE TIME OF DAY 2
@dp.message_handler(state=DiscoverFreeTime.output)
async def output_free_time(message: types.message, state: FSMContext):
    await get_output_free_time(message, state)


# CALCULATE THE SCORE
@dp.message_handler(Text(equals=calculator_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def calculate_score(message: types.message):
    await message.answer('Напишите ваш рейтинг допуска')
    await Calculate.score.set()


# SHOW ALL SUBJECTS
@dp.message_handler(Text(equals=subjects_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def show_all_subjects(message: types.message, state: FSMContext):
    subjects = await get_subjects(message)
    async with state.proxy() as data:
        data['subjects'] = subjects
    print(subjects)
    await message.answer('Все ваши предметы', reply_markup=createButtons(subjects))
    await Subjects.select_task.set()


# SUBJECTS CANCEL
@dp.message_handler(Text(equals=cancel_str,
                         ignore_case=True),
                    state=Subjects.states)
async def show_all_subjects(message: types.message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=await stud_kb(state))
    await state.reset_data()
    await StudentStates.student.set()


# TASK SELECT
@dp.message_handler(state=Subjects.select_task)
async def show_all_subjects(message: types.message, state: FSMContext):
    subject = message.text
    subjects = (await state.get_data())['subjects']
    if subject in subjects:
        tasks = await get_tasks_of_subject(message, subject)
        tasks_list = [name_task for name_task in tasks]
        await message.answer(f"Задания - \"{subject}\"", reply_markup=createButtons(tasks_list))
        async with state.proxy() as data:
            data['tasks'] = tasks
            data['subject'] = subject
        await Subjects.next()
    else:
        await message.answer("Выберите предмет из списка!", reply_markup=createButtons(subjects))


##################################
# BIG BLOCK ABOUT TAKE THE VARIANT
##################################
# TASK MENU
@dp.message_handler(state=Subjects.task_menu)
async def take_variant_start(message: types.message, state: FSMContext):
    if message.text in (await state.get_data())['tasks']:
        await message.answer(f"Что хотите сделать с заданием - \"{message.text}\"?", reply_markup=task_menu_kb)
        async with state.proxy() as data:
            data['task'] = message.text
            data['task_id'] = data['tasks'][message.text]
        await Subjects.next()
    else:
        await message.answer(f"Выберите один из тасков ниже")


# SELECT MENU ITEM -> SHOW TASK INFO
@dp.message_handler(Text(equals=show_task_info_str, ignore_case=True), state=Subjects.select_item_menu)
async def take_variant_start(message: types.message, state: FSMContext):
    media_group = types.MediaGroup()
    async with state.proxy() as data:
        pass
    task_id = data['task_id']
    task_info, photo_id, document_id = await get_task_info(task_id)
    for pic in photo_id:
        print(pic)
        media_group.attach(({"media": pic[0][:-1], "type": 'photo'}))
    for doc in document_id:
        await message.answer_document(doc[0])
    if not media_group:
        await message.answer_media_group(media_group)
    await message.answer(text=task_info, reply_markup=task_menu_kb)
    await Subjects.select_item_menu.set()


# SELECT MENU ITEM -> TAKE VARIANT
@dp.message_handler(Text(equals=take_variant_str, ignore_case=True), state=Subjects.select_item_menu)
async def take_variant_start(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        pass
    task_id = data['task_id']
    variants = await get_taken_variants(task_id)
    range_variants = await get_range_variants(task_id)
    if variants is None:
        await message.answer("У данной работы нет вариантов")
        await Subjects.select_item_menu.set()
        return False
    if await check_taken_yet_variant(message, variants):
        await message.answer("Вы уже заняли вариант этой работы")
        return False
    variants_list = [var for var in variants]
    print(f'variants_list: {variants_list}')
    async with state.proxy() as data:
        data['variants'] = variants
        data['range_variants'] = range_variants
    await message.answer(f'Напишите вариант который желаете занять.\n'
                         f'Имеющиеся варианты: {range_variants[0]}-{range_variants[1]}\n'
                         f'{inaccessible_variants_output(variants)}')
    await TakeVariant.confirm_to_take_variant.set()


# TAKE VARIANT CANCEL
@dp.message_handler(Text(equals=cancel_str, ignore_case=True), state=TakeVariant.states)
async def take_variant_cancel(message: types.message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=await stud_kb(state))
    await state.reset_data()
    await StudentStates.student.set()


# TAKE VARIANT CONFIRM
@dp.message_handler(state=TakeVariant.confirm_to_take_variant)
async def take_variant_start(message: types.message, state: FSMContext):
    if message.text.isdigit():
        msg = int(message.text)
        async with state.proxy() as data:
            pass
        task_id = data['task_id']
        variants = data['variants']
        if await check_available_variant(task_id=task_id, variant=msg, all_variants=variants, msg=message):
            await add_variant(task_id=task_id, msg=message)
            varinats_info = await get_taken_variants(task_id)
            await message.answer(f'Вы заняли вариант\n'
                                 f'{taken_variants_output(varinats_info)}', reply_markup=task_menu_kb)
        else:
            '''
                In one moment some users can take the same variant. Need view logs 
            '''
            await message.answer("Данный вариант занят или вовсе отсутствует", reply_markup=task_menu_kb)
        await Subjects.select_item_menu.set()
    else:
        await message.answer('Введите номер варианта!')


# GET USERS AND VARIANTS
@dp.message_handler(Text(equals=show_variant_of_task_str, ignore_case=True), state=Subjects.select_item_menu)
async def variants_and_users(message: types.message, state: FSMContext):
    task_id = (await state.get_data())['task_id']
    users_dict = await get_variants_and_users(task_id, message)
    if not users_dict:
        await message.answer('Варианты еще никто не занимал')
    else:
        await message.answer(f'Вариант - студент:\n{users_dict}')


# TAKE AWAY VARIANT
@dp.message_handler(Text(equals=take_away_variant_str, ignore_case=True), state=Subjects.select_item_menu)
async def take_away_variant(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        pass
    task_id = data['task_id']
    variants = await get_taken_variants(task_id)
    if variants is None:
        await message.answer("У данной работы нет вариантов")
        await Subjects.select_item_menu.set()
        return 0
    async with state.proxy() as data:
        data['variants'] = variants
    if await check_busy_variant(task_id, message):
        await message.answer("Вы действительно хотите освободить вариант?", reply_markup=question_kb)
        await TakeAwayVariant.confirm.set()
    else:
        await message.answer('Вы не занимали вариант', reply_markup=task_menu_kb)


# PLUG FOR SUBJECT
@dp.message_handler(state=Subjects.select_item_menu)
async def subject_plug(message: types.message, state: FSMContext):
    await message.answer('Что вы хотите сделать с заданием?', reply_markup=task_menu_kb)


# TAKE AWAY VARIANT CONFIRM
@dp.message_handler(state=TakeAwayVariant.confirm)
async def take_away_variant_confirm(message: types.message, state: FSMContext):
    if message.text == yes_str or message.text == no_str:
        async with state.proxy() as data:
            pass
        if message.text == yes_str:
            await release_variant(data['task_id'], message)
            await message.answer('Вариант освобожден!', reply_markup=task_menu_kb)
            logger.info(f'User - {message.chat.id} release variant')
            await Subjects.select_item_menu.set()
        elif message.text == no_str:
            await message.answer('Вариант остался прикреплен за вами.', reply_markup=task_menu_kb)
            await Subjects.select_item_menu.set()
    else:
        await message.answer('Принимается только "Да" или "Нет"')


# INPUT SCORE
@dp.message_handler(state=Calculate.score)
async def calculate_score(message: types.message, state: FSMContext):
    if message.text.isdigit():
        score = calc_basic(int(message.text))
        await message.answer(score, reply_markup=await stud_kb(state))
    else:
        await message.answer('Неверный ввод!', reply_markup=await stud_kb(state))
    await StudentStates.student.set()


# GET INFO ABOUT STUDENT
@dp.message_handler(commands=['bio'], state=StudentStates.student)
async def bio(message: types.Message):
    result = await get_bio(message.chat.id)
    await message.answer(result)


# DELETE USER ACCOUNT
@dp.message_handler(commands=['deleteme'], state=StudentStates.student)
async def deleteme(message: types.Message):
    await delete_user(message)


# GET HELP FOR STUDENT
@dp.message_handler(commands=['help'], state=StudentStates.student)
async def check_user(message: types.Message):
    await message.answer(help_user_text)


# GET CURRENT TIME
@dp.message_handler(commands=['time'], state=StudentStates.student)
async def output_current_time(message: types.Message):
    await message.answer(str(datetime.datetime.now()))


# GET CLASSMATES
@dp.message_handler(commands=['classmates'], state=StudentStates.student)
async def classmates(message: types.Message):
    await message.answer(await get_list_of_classmates(message.chat.id))


# CAPTAIN ZONE
@dp.message_handler(commands=['help_captain'], state=StudentStates.student)
async def help_captain_privilege(message: types.Message):
    await message.answer(help_captain_str)


# TAKE PRIVILEGE
@dp.message_handler(commands=['captain_privilege'], state=StudentStates.student)
async def captain_privilege(message: types.Message):
    await message.answer('Введите пожалуйста ключ')
    await SetCaptainState.set.set()


# NO COMMAND
@dp.message_handler(state=StudentStates.student)
async def get_menu(message: types.Message, state: FSMContext):
    await message.answer(text='Я не понимаю что вы хотите', reply_markup=await stud_kb(state))
