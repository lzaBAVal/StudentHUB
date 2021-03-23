import base64
import re

import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils.exceptions import Throttled

import datetime
import keys
from bot import keyboard as kb
from bot.states.states import AnonStates, RegistrationStates, StudentStates, TesterState, AddLesson, DeleteLesson
from functions.find_group import group_search
from loader import dp, db, bot
from logs.logging_core import init_logger
from schedule_json.change.change_sched import add_lesson
from schedule_json.change.change_sched import get_free_time, get_lessons_time, delete_lesson
from schedule_json.harvest.harvest_main import harvest_arhit_sched, harvest_spec_group, harvest_spec_arhit_sched
from schedule_json.output.get_schedule_object import get_sched_type, get_sched
from vars import WeekDays_RU, special_chars, special_chars_digit


logger = init_logger()

'''
# ERRORS
@dp.errors_handler()
async def errors_handler(update, exception, message: types.Message):
    logger.exception(f'Update: {update} \n{exception}')
'''


# NONE
@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await TesterState.tester.set()
    await message.answer(text='Привет, студент! Я бот \nНа данный момент идет тестовый период моей работы.\
    \nЯ могу ошибаться, тормозить в общем работать не так как нужно)\
    \nЕсли ты хочешь пользоваться моим функционалом или помочь мне, тогда тебе нужен ключик для входа\
    \nЕго можно взять у моего разработчика или админов \
    \nЕсли уже есть ключик то жмакай на кнопку ввести ключ и вводи его)\
    \nРазработчик будет очень рад если ты будешь отправлять ему замечания по поводу моей работы!',
                         reply_markup=kb.tester_kb)


@dp.message_handler(state=None)
async def def_user(message: types.Message):
    try:
        if not (await db.check_user(message.chat.id)):
            await AnonStates.anon.set()
            await message.answer(text='Анон.', reply_markup=kb.anon_kb)
        else:
            await StudentStates.student.set()
            await message.answer(text='Повторите ваш запрос', reply_markup=kb.stud_kb)
    except Exception as exc:
        logger.exception(exc)
        await message.answer(text='Что то пошло не так! Ошибка', reply_markup=kb.anon_kb)


# ALL ------------------------------------------------------------------------
'''
@dp.message_handler(commands=['help'], state='*')
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/voice test', '/photo', '/group', '/note', '/file', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
'''

'''
@dp.message_handler(commands=['update_spec_group'], state='*')
async def update_spec_group(message: types.Message):
    await harvest_spec_group(db)


@dp.message_handler(commands=['update_spec_sched'], state='*')
async def update_spec_sched(message: types.Message):
    await harvest_spec_arhit_sched(db)
'''


'''
@dp.message_handler(commands=['addhash'], state='*')
async def add_hash(message: types.Message):
    hash = await keys.create_hashes(db)
    await message.answer(text=hash)
'''


@dp.message_handler(commands=['id'], state='*')
async def chat_id(message: types.Message):
    await message.answer(text=message.chat.id)


'''
@dp.message_handler(commands=['error'], state='*')
async def chat_id(message: types.Message):
    await message.answer(text=str(0/0))
'''


@dp.message_handler(commands=['trot'], state='*')
async def send_welcome(message: types.Message):
    try:
        # Execute throttling manager with rate-limit equal to 2 seconds for key "start"
        await dp.throttle('start', rate=5)
    except Throttled:
        # If request is throttled, the `Throttled` exception will be raised
        await message.reply('Too many requests!')
    else:
        # Otherwise do something
        await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


# TESTER ------------------------------------------------------------------------
'''
@dp.message_handler(text='У меня есть ключ', state=TesterState.tester)
async def start_add_tester(message: types.Message):
    await TesterState.start_add.set()
    await message.answer(text='Вводите его')


@dp.message_handler(state=TesterState.start_add)
async def start_add_tester(message: types.Message):
    try:
        await keys.add_tester(db, message.chat.id, message.text)
        await TesterState.next()
    except Exception as exc:
        logger.exception(exc)
        await message.answer(text='Проверьте еще раз вводимый ключ. Что то пошло не так.')
    await message.answer(text='Для подтверждения нажмите на котика', reply_markup=kb.cat_kb)


@dp.message_handler(state=TesterState.finish_add)
async def start_add_tester(message: types.Message):
    logger.info('New hash has benn added. User - ' + str(message.chat.id))
    await message.answer(text='Отлично теперь Вы являетесь членом команды тестировщиков, спасибо Вам!\
    \nДалее чтобы получить доступ к моему функционалу нужно лишь пройти простую регистрацию.', reply_markup=kb.anon_kb)
    await AnonStates.anon.set()
'''

# ANON ------------------------------------------------------------------------
@dp.message_handler(state=AnonStates.anon, text='Регистрация')
async def reg_start(message: types.Message):
    await RegistrationStates.name.set()
    await message.answer(text='Введите ваше имя', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AnonStates.anon)
async def anon_message(message: types.Message):
    await message.answer(
        text='На данный момент я вас не знаю, пройдите регистрацию чтобы получить доступ к моему функционалу',
        reply_markup=kb.anon_kb)


# STUDENT ------------------------------------------------------------------------
@dp.message_handler(text='Вернуться на главное меню', state=StudentStates.student)
async def all_shedule(message: types.Message):
    await message.answer('Вы в главном меню', reply_markup=kb.stud_kb)

@dp.message_handler(text='Все расписание', state=StudentStates.student)
async def all_shedule(message: types.Message):
    try:
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=1)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось показать расписание, сообщите об этом админу.')
    else:
        await message.answer(text=resp)


@dp.message_handler(text='Расписание на сегодня', state=StudentStates.student)
async def todays_shedule(message: types.Message):
    try:
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=2)
        if resp == -1:
            await message.answer('Не удалось показать расписание, сообщите об этом админу.')
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось показать расписание, сообщите об этом админу.')
    else:
        await message.answer(text=resp)


@dp.message_handler(text='Cледующая пара', state=StudentStates.student)
async def next_lesson(message: types.Message):
    try:
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=3)
        if resp == -1:
            await message.answer('Не удалось показать расписание, сообщите об этом админу.')
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось показать расписание, сообщите об этом админу.')
    else:
        await message.answer(text=resp)


@dp.message_handler(text='Расписание на завтра', state=StudentStates.student)
async def tommorow_lesson(message: types.Message):
    try:
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=4)
        if resp == -1:
            await message.answer('Не удалось показать расписание, сообщите об этом админу.')
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось показать расписание, сообщите об этом админу.')
    else:
        await message.answer(text=resp)


@dp.message_handler(text='Изменить расписание', state=StudentStates.student)
async def change_sched(message: types.message):
    await message.answer('Что вы хотите сделать с расписанием?', reply_markup=kb.change_sched_kb)


@dp.message_handler(text='Добавить урок', state=StudentStates.student)
async def add_lesson_start(message: types.message):
    await message.answer('В какой день вы хотите добавить урок?', reply_markup=kb.days())
    await AddLesson.time.set()


@dp.message_handler(state=AddLesson.time)
async def add_lesson_time(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if message.text.lower() not in WeekDays_RU:
            await message.answer(text='Введите день недели!')
            await add_lesson_start(message)
            return 0
        sched = await get_sched(message.chat.id)
        free_time = await get_free_time(message.text.lower(), sched)
        async with state.proxy() as data:
            data['day'] = message.text.lower()
            data['sched'] = sched
            data['free_time'] = free_time
    data = await state.get_data()
    await message.answer('Есть свободные часы в этот день: ', reply_markup=kb.free_time(data['free_time']))
    await AddLesson.next()


@dp.message_handler(state=AddLesson.lesson)
async def add_lesson_lesson(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        data = await state.get_data()
        if message.text not in data['free_time']:
            await message.answer(text='Введите время на которое хотите назначить урок!')
            await AddLesson.time.set()
            await add_lesson_time(message, state, completed=True)
            return 0

        async with state.proxy() as data:
            data['time'] = message.text
    await message.answer('Введите название урока')
    await AddLesson.next()


@dp.message_handler(state=AddLesson.teacher)
async def add_lesson_teacher(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 30 and not re.match(special_chars, message.text):
            async with state.proxy() as data:
                data['lesson'] = message.text
        else:
            await message.answer(text='Название урока должно быть меньше 30 символов и состоять только из букв и цифр!')
            await AddLesson.lesson.set()
            await add_lesson_lesson(message, state, completed=True)
            return 0
    await message.answer('Введите имя преподавателя')
    await AddLesson.next()


@dp.message_handler(state=AddLesson.subgroup)
async def add_lesson_subgroup(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 30 and not re.match(special_chars_digit, message.text):
            async with state.proxy() as data:
                data['teacher'] = message.text
        else:
            await message.answer(text='Имя преподавателя должно быть меньше 30 символов и состоять только из букв!')
            await AddLesson.teacher.set()
            await add_lesson_teacher(message, state, completed=True)
            return 0
    await message.answer('Введите подгруппу', reply_markup=kb.subgroup_kb)
    await AddLesson.next()


@dp.message_handler(state=AddLesson.classroom)
async def add_lesson_classroom(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if message.text.lower() == 'нет подгрупп' and not re.match(special_chars, message.text) or \
                re.match(r'\d', message.text):
            async with state.proxy() as data:
                data['subgroup'] = message.text
        else:
            await message.answer(text='Введите либо номер подгруппы либо укажите что подгрупп нет')
            await AddLesson.subgroup.set()
            await add_lesson_subgroup(message, state, completed=True)
            return 0
    await message.answer('Введите номер кабинета или укажите что вы учитесь онлайн', reply_markup=kb.classroom_kb)
    await AddLesson.next()


@dp.message_handler(state=AddLesson.check)
async def add_lesson_check(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 10 and not re.match(special_chars, message.text) or \
                message.text.lower() == 'онлайн':
            async with state.proxy() as data:
                data['classroom'] = message.text
            await message.answer(
                f"Проверьте данные: \nДень: {data['day']}\nВремя: {data['time']}\nУрок: {data['lesson']}\n"
                f"Преподаватель: {data['teacher']} "
                f"\nПодгруппа: {data['subgroup']}\nКабинет: {data['classroom']}\n\nВсе верно?",
                reply_markup=kb.question_kb)
        else:
            await message.answer(
                text='Требуется наименование кабинет. Не более 10 символов или укажите что вы учитесь онлайн')
            await AddLesson.classroom.set()
            await add_lesson_classroom(message, state, completed=True)
            return 0

    await AddLesson.next()


@dp.message_handler(lambda message: message.text.lower() == "да", state=AddLesson.process)
async def add_lesson_process(message: types.message, state: FSMContext):
    data = await state.get_data()
    sched = await add_lesson(sched=data['sched'], day=WeekDays_RU.index(data['day']), complex_time=data['time'],
                             classroom=data['classroom'], name_lesson=data['lesson'], teacher=data['teacher'])
    sched = str(base64.b64encode(str(sched.dict()).encode('utf-8')))[2:-1]
    await db.update_group_sched(sched, message.chat.id)
    await AddLesson.next()
    await message.answer('Идет процесс занесения урока в базу! Для завершения тыкните на котика',
                         reply_markup=kb.cat_kb)


@dp.message_handler(lambda message: message.text.lower() == "нет", state=AddLesson.process)
async def add_lesson_process_no(message: types.message, state: FSMContext):
    await message.answer(text='Добавьте урок заново')
    await state.finish()
    await StudentStates.student


@dp.message_handler(state=AddLesson.final)
async def add_lesson_process_yes(message: types.message, state: FSMContext):
    await message.answer('Урок добавлен', reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(text='Убрать урок', state=StudentStates.student)
async def add_lesson_process_yes(message: types.message):
    await message.answer('Выберите день:', reply_markup=kb.days())
    await DeleteLesson.lesson.set()


@dp.message_handler(state=DeleteLesson.lesson)
async def add_lesson_process_yes(message: types.message, state: FSMContext):
    sched = await get_sched(message.chat.id)
    async with state.proxy() as data:
        data['day'] = message.text.lower()
        data['sched'] = sched
    lessons_time: list = await get_lessons_time(data['day'], sched)
    await message.answer('Какой предмет вы желаете удалить?', reply_markup=kb.free_time(lessons_time))
    await DeleteLesson.next()


@dp.message_handler(state=DeleteLesson.check)
async def delete_lesson_check(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['deletelesson'] = message.text

    await message.answer('Вы уверены что вы хотите удалить "' + data['deletelesson'] + '" из расписания?',
                         reply_markup=kb.question_kb)
    await DeleteLesson.next()


@dp.message_handler(lambda message: message.text.lower() == "да", state=DeleteLesson.process)
async def delete_lesson_check(message: types.message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        'Идет процесс удаления урока из расписания... \n Тыкните на котика чтобы завержить процесс удаления',
        reply_markup=kb.cat_kb)
    new_sched = delete_lesson(data['sched'], data['deletelesson'], day=data['day'])
    print(new_sched)
    await db.update_group_sched(new_sched, message.chat.id)
    await DeleteLesson.next()


@dp.message_handler(lambda message: message.text.lower() == "нет", state=DeleteLesson.process)
async def delete_lesson_check(message: types.message, state: FSMContext):
    await message.answer('Вы отменили процесс удаления',
                         reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=DeleteLesson.final)
async def delete_lesson_check(message: types.message, state: FSMContext):
    await message.answer('Вы удалили урок из расписания',
                         reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(commands=['addhash'], state=StudentStates.student)
async def add_hash(message: types.Message):
    if message.chat.id == 690976128 or message.chat.id == 842781422:
        try:
            hash = await keys.create_hashes(db)
        except Exception as exc:
            logger.exception(exc)
            await message.answer('ERROR: Не удалось создать хэш.')
        else:
            await message.answer(text=hash)


@dp.message_handler(commands=['deleteme'], state=StudentStates.student)
async def next_lesson(message: types.Message):
    try:
        await db.delete_account(message.chat.id)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Мне не удалось удалить ваш аккаунт, сообщите об этом админу')
    else:
        await AnonStates.anon.set()
        await message.answer('Ваш аккаунт был удален.', reply_markup=kb.anon_kb)


@dp.message_handler(commands=['time'], state=StudentStates.student)
async def next_lesson(message: types.Message):
    await message.answer(str(datetime.datetime.now()), reply_markup=kb.stud_kb)


@dp.message_handler(state=StudentStates.student)
async def get_menu(message: types.Message):
    await message.answer(text='На данный момент доступен только просмотр расписания!', reply_markup=kb.stud_kb)


# REGISTRATION ------------------------------------------------------------------------
@dp.message_handler(state=RegistrationStates, text='Отменить регистрацию')
async def reg_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await AnonStates.anon.set()
    await message.answer('Регистрация отменена', reply_markup=kb.anon_kb)


@dp.message_handler(state=RegistrationStates.name)
async def reg_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await RegistrationStates.next()
    await message.answer(text='Введите вашу фамилию', reply_markup=kb.register_kb)


@dp.message_handler(state=RegistrationStates.surname)
async def reg_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await RegistrationStates.next()
    await message.answer(text='Введите наименование вашей группы. Вы должны ввести строку вида \'сиб 19 6\'')


@dp.message_handler(state=RegistrationStates.find_group)
async def search_group(message: types.Message):
    result = await group_search(message.text)
    logger.info('Client is finding himself group - ' + str(str(message.text).encode('utf-8')))
    if result == -1:
        await message.answer(
            text='Не могу разобрать что вы пишите, попробуйте снова. Напомню, наименование группы должно быть такого '
                 'формата - "cиб 19 6"')
    else:
        comp_match, match, other_match = result
        if comp_match:
            kboard = kb.createButtons(comp_match)
            await message.answer(text='Это наименование вашей группы?', reply_markup=kboard)
            await RegistrationStates.next()
        elif match:
            kboard = kb.createButtons(match)
            await message.answer(text='Не найдено точное наименование вашей группы. Ваша группа есть в этом списке?',
                                 reply_markup=kboard)
            # await RegistrationStates.next()
        elif other_match:
            kboard = kb.createButtons(other_match)
            await message.answer(
                text='Я не нашел ничего похожего. Посмотрите список групп который я вам предоставил. Возможно там '
                     'будет то что вам нужно',
                reply_markup=kboard)
            # await RegistrationStates.next()
        else:
            await message.answer(
                text='Вашей группы у меня нет. Если вы уверены что верно вводите название группы, напишите об этом '
                     'разработчику, он вам поможет',
                reply_markup=kb.anon_kb)
            await AnonStates.anon.set()


@dp.message_handler(state=RegistrationStates.accept_all_data)
async def accept_all_data(message: types.Message, state: FSMContext):
    try:
        group_id = await db.get_group_id(message.text)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('ERROR: произошла ошибка. Регистрация отменена')
        await state.finish()
        await AnonStates.anon.set()
    else:
        group_id = dict(group_id)['id_inc']
        async with state.proxy() as data:
            data['group_name'] = message.text
            data['group_id'] = group_id
        await message.answer(text='Проверьте все ваши данные. Все правильно?', reply_markup=kb.question_kb)
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Имя,', data['name']),
                md.text('Фамилия:', data['surname']),
                md.text('Группа:', data['group_name']),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        await RegistrationStates.next()


@dp.message_handler(state=RegistrationStates.insert_sql, text='Да')
async def reg_final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await db.add_user(message.chat.id, data['name'], data['surname'], str(data['group_id']))
    except Exception as e:
        print(e)
        await message.answer(text='Произошла ошибка, обратитесь к разработчику)', reply_markup=kb.anon_kb)
        logger.exception()
        await state.finish()
        await AnonStates.anon.set()
    else:
        await message.answer(text='Идет процесс регистрации...\nДля завершения нажми на котика)',
                             reply_markup=kb.cat_kb)
        await RegistrationStates.next()


@dp.message_handler(state=RegistrationStates.final)
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Все отлично! Теперь вы зарегестрированы.', reply_markup=kb.stud_kb)
    data = await state.get_data()
    logger.info('New user: Name - ' + str(str(data['name']).encode('utf-8')) + ', surname - ' + str(
        str(data['surname']).encode('utf-8')) + ', group - ' + str(str(data['group_id']).encode('utf-8')))
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=RegistrationStates.insert_sql, text='Нет')
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Пройдите регистрацию заново!', reply_markup=kb.anon_kb)
    await state.finish()
    await AnonStates.anon.set()


# END -----------------------------------------------------------


'''
# This block of code is a test harvest the groups and schedules 

@dp.message_handler(commands=['update1'], state='*')
async def chat_id(message: types.Message):
    await harvest_groups(db)


@dp.message_handler(commands=['update2'], state='*')
async def chat_id(message: types.Message):
    await harvest_arhit_sched(db)
'''

# @dp.message_handler(commands=['linebut'])
# async def inlinebutton(message: types.Message):
#    await message.reply('Первая инлайн кнопка', reply_markup=kb.inline_kb1)


'''
@dp.message_handler(commands=['setstate'])
async def process_setstate(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)
'''

'''
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_query(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
'''
