from datetime import date, datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.keyboard.keyboard import stud_kb, cancel_kb, skip_kb, skip_finish_kb, question_kb, createButtons, \
    show_subjects_kb, show_tasks_kb, subject_kb
from bot.states.states import StudentStates, SetCaptainState, CreateNewTask, ShowTask, DeleteTask, \
    DeleteSubject, AddSubject
from bot.strings.commands import *

from functions.captain.keys import add_captain
from functions.command import cancel
from functions.other.parse_variants import parse_variant
from functions.student.add_document import keep_document, save_document
from functions.student.add_photo import save_photo, keep_photo

from loader import db
from misc import dp, bot
from models import Student, Task, Subject
from task_subject.harvest import add_object_for_group, add_subject
from task_subject.education import deleteSubject
from task_subject.education import get_all_tasks, get_subjects, exclude_variant, check_existed_task, get_task_info
from utils.log.logging_core import init_logger

logger = init_logger()


@dp.message_handler(text=back_to_menu_str, state=SetCaptainState.states)
async def cancel_captain(message: types.Message, state: FSMContext):
    await cancel(message, state)


# SET CAPTAIN PRIVILEGE
@dp.message_handler(state=SetCaptainState.set)
async def set_captain(message: types.Message):
    hash = message.text.strip()
    if len(hash) == 32:
        code = await add_captain(db, message.chat.id, hash)
        if code == -1:
            await message.answer('Не удалось добавить ваш ключ, сообщите об этом старосте', reply_markup=stud_kb())
        else:
            await message.answer('Отлично, теперь у вас есть права старосты.', reply_markup=stud_kb())
            try:
                result = await add_object_for_group(message)
                if result == -1:
                    raise Exception
            except Exception as exc:
                logger.warn(f'Captain with chat_id {message.chat.id} can\'t create task_subject pull')
                logger.exception(exc)
    else:
        await message.answer('Вы отправляете мне сомнительный ключ, проверьте правильно ли вы его вводите '
                             'или обратитесь к админам\nВы в главном меню', reply_markup=stud_kb())
    await StudentStates.student.set()


# TODO CreateNewTask
# TODO RestrictAmountPhotos - 10
# CANCEL CREATE TASK
@dp.message_handler(Text(equals=cancel_str,
                         ignore_case=True),
                    state=CreateNewTask.states,
                    is_captain=True)
async def cancel_add_task(message: types.Message):
    await message.answer('Вы отменили процесс добавления задания', reply_markup=stud_kb())
    await StudentStates.student.set()


# CREATE TASK
@dp.message_handler(Text(equals=add_task_str,
                         ignore_case=True),
                    state=StudentStates.student,
                    is_captain=True)
async def object_name(message: types.Message):
    subject_buttons = createButtons(await get_subjects(message))
    await message.answer('Для какого предмета вы добавляете задание? Выберите из списка ниже один из предметов, '
                         'в случае если нужного нет, введите название предмета, оно будет добавлено в pull предметов '
                         'группы.',
                         reply_markup=subject_buttons)
    await CreateNewTask.name.set()


@dp.message_handler(state=CreateNewTask.name,
                    is_captain=True)
async def task_name(message: types.Message, state: FSMContext):
    student_id = await Student.filter(chat_id=message.chat.id).values_list('id')
    student_id = student_id[0][0]
    if not (await Subject.filter(name=message.text, user_id=student_id)) == []:
        async with state.proxy() as data:
            data['task_subject'] = message.text
        await message.answer('Введите название для задания (РГР, СРС, лабораторная работа), номер работы',
                             reply_markup=cancel_kb)
        await CreateNewTask.next()
    else:
        await message.answer(f'Вы хотите добавить новый предмет {message.text}?')
        await CreateNewTask.create_subject.set()


@dp.message_handler(Text(equals='Да',
                         ignore_case=True),
                    state=CreateNewTask.create_subject,
                    is_captain=True)
async def create_new_subject(message: types.Message, state: FSMContext):
    await object_name(message)


@dp.message_handler(Text(equals='Нет',
                         ignore_case=True),
                    state=CreateNewTask.create_subject,
                    is_captain=True)
async def create_new_subject(message: types.Message, state: FSMContext):
    await add_subject([message.text], message)
    await message.answer(f'Вы добавили новый предмет в pull предметов группы')
    await object_name(message)


@dp.message_handler(is_captain=True,
                    state=CreateNewTask.description)
async def academic_work_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    response_user = await Student.filter(chat_id=message.chat.id).values_list('id', 'group_id')
    response_user = response_user[0]
    subject_id = await Subject.filter(name=data['task_subject'], user_id=response_user[0]).values_list('id')
    subject_id = subject_id[0][0]
    if await check_existed_task(message.text, subject_id):
        await message.answer(f'Задание с таким именем уже существует, дайте другое имя заданию!')
        return 0
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание для данной работы или оставьте пометки для студентов. '
                         f'Если нет необходиости что то писать нажмите на кнопку \"{skip_str}\".',
                         reply_markup=skip_kb)
    await CreateNewTask.next()


@dp.message_handler(is_captain=True,
                    state=CreateNewTask.variants)
async def academic_work_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = ''
    if message.text.lower() == skip_str:
        async with state.proxy() as data:
            data['description'] = message.text
    await message.answer('Напишите варианты, которые студенты могут использовать в этой работе.\n'
                         'Пример: 1-40\nЕсли есть варианты которые нужно исключить введите их через пробел\n'
                         'Пример: 3-39 2 4 8 19\nСтуденты не смогут занимать варианты работ под номерами 2, 4, 8, 19\n'
                         f'Если данная работа не предусматривает варианты нажмите \"{skip_str}\"',
                         reply_markup=skip_kb)
    await CreateNewTask.next()


@dp.message_handler(is_captain=True,
                    state=CreateNewTask.photo_start)
async def academic_work_add_photo(message: types.Message, state: FSMContext):
    # TODO Write script which parse variants
    # ...
    if message.text != skip_str:
        variants = parse_variant(message.text)
        if variants == 1:
            await message.answer('Вы не верно ввели варианты работ. Попробуйте снова.\n'
                                 'Пример: 3-39 2 4 8 19')
            await CreateNewTask.photo_start.set()
            return 0
        async with state.proxy() as data:
            data['var_start'] = variants[0]
            data['var_end'] = variants[1]
            data['var_exclude'] = variants[2]
            data['photo_count'] = 0
            data['document_count'] = 0
    else:
        async with state.proxy() as data:
            data['var_start'] = 'pass'
            data['photo_count'] = 0
            data['document_count'] = 0
    await message.answer("Отправляйте фотографии боту. "
                         "В случае если вы все отправили или в этом нет необходимости, "
                         f"нажмите на кнопку \"{skip_finish_str}\"", reply_markup=skip_finish_kb)
    await CreateNewTask.next()


# UPLOAD PHOTO
@dp.message_handler(content_types=['photo'], state=CreateNewTask.photo_upload)
async def upload_photo(message: types.Message, state: FSMContext):
    hash = await keep_photo(message)
    data = await state.get_data()
    data['photo_count'] += 1
    key = f'photo_{data["photo_count"]}'
    data[key] = hash
    await state.update_data(data=data)


# UPLOAD DOCUMENT
@dp.message_handler(content_types=['document'], state=CreateNewTask.photo_upload)
async def upload_document(message: types.Message, state: FSMContext):
    hash = await keep_document(message)
    data = await state.get_data()
    data['document_count'] += 1
    key = f'document_{data["document_count"]}'
    data[key] = hash
    await state.update_data(data=data)


@dp.message_handler(Text(equals=[skip_finish_str, skip_str],
                         ignore_case=True),
                    is_captain=True,
                    state=CreateNewTask.photo_upload)
async def academic_work_confirm(message: types.Message):
    await message.answer('Проверьте введенные вами данные, все верно?"', reply_markup=question_kb)
    await CreateNewTask.next()


@dp.message_handler(Text(equals=no_str,
                         ignore_case=True),
                    is_captain=True,
                    state=CreateNewTask.check_question)
async def academic_work_confirm_no(message: types.Message, state: FSMContext):
    await message.answer('Добавьте задание заново', reply_markup=stud_kb())
    await state.reset_data()
    await StudentStates.student.set()


@dp.message_handler(Text(equals=yes_str, ignore_case=True),
                    is_captain=True,
                    state=CreateNewTask.check_question)
async def academic_work_confirm_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    response_user = await Student.filter(chat_id=message.chat.id).values_list('id', 'group_id')
    response_user = response_user[0]
    subject_id = await Subject.filter(name=data['task_subject'], user_id=response_user[0]).values_list('id')
    subject_id = subject_id[0][0]
    if data['var_start'] != 'pass':
        await Task(name=data['name'],
                   description=data['description'],
                   subject_id=subject_id,
                   variant_start=data['var_start'],
                   variant_end=data['var_end'],
                   user_variant=exclude_variant(data['var_exclude'])).save()
    else:
        await Task(name=data['name'],
                   subject_id=subject_id).save()

    task_id = await Task.filter(name=data['name'],
                                subject_id=subject_id).values_list('id')
    task_id = task_id[0][0]
    for photo_id in range(data['photo_count']):
        await save_photo(task_id, data[f"photo_{photo_id + 1}"])
    for doc_id in range(data['document_count']):
        await save_document(task_id, data[f"document_{doc_id + 1}"])
    await message.answer('Ваше задание было успешно добавлено!', reply_markup=stud_kb())
    await state.reset_data()
    await StudentStates.student.set()


# DELETE TASK CHOOSE
@dp.message_handler(Text(equals=delete_task_str, ignore_case=True), state=StudentStates.student)
async def delete_task(message: types.Message, state: FSMContext):
    await message.answer('Выберите таск который хотите удалить')
    await show_academic_tasks(message, state)
    await DeleteTask.question.set()


# DELETE TASK NO
@dp.message_handler(Text(equals=cancel_str, ignore_case=True), state=DeleteTask.states)
async def delete_task(message: types.Message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=stud_kb())
    await state.reset_data()
    await StudentStates.student.set()


# DELETE TASK CONFIRMATION
@dp.message_handler(state=DeleteTask.question)
async def delete_task(message: types.Message, state: FSMContext):
    await message.answer('Вы уверены что хотите удалить этот таск?', reply_markup=question_kb)
    data = await state.get_data()
    for task in data['tasks']:
        if message.text == task:
            task_id = data['tasks'][task]
            data['task_id'] = task_id
            await state.update_data(data)
    await DeleteTask.next()


# DELETE TASK YES
@dp.message_handler(Text(equals=yes_str, ignore_case=True), state=DeleteTask.confirm)
async def delete_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Идет процесс удаления таска...')
    await Task.filter(id=data['task_id']).delete()
    await message.answer('Таск удален', reply_markup=stud_kb())
    await state.reset_data()
    await StudentStates.student.set()


# DELETE TASK NO
@dp.message_handler(Text(equals=no_str, ignore_case=True), state=DeleteTask.confirm)
async def delete_task(message: types.Message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=stud_kb())
    await state.reset_data()
    await StudentStates.student.set()


# SHOW ALL ACADEMIC TASKS
@dp.message_handler(Text(equals=show_tasks_str, ignore_case=True), state=StudentStates.student)
async def show_academic_tasks(message: types.Message, state: FSMContext):
    obj_task = await get_all_tasks(message)
    markup, tasks = show_tasks_kb(obj_task)
    async with state.proxy() as data:
        data['tasks'] = tasks
    await message.answer('Все таски', reply_markup=markup)
    await ShowTask.choose.set()


@dp.message_handler(Text(equals=cancel_str, ignore_case=True), state=ShowTask.choose)
async def show_one_academic_task(message: types.Message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=stud_kb())
    await state.reset_data()
    await StudentStates.student.set()


@dp.message_handler(state=ShowTask.choose)
async def show_one_academic_task(message: types.Message, state: FSMContext):
    media_group = types.MediaGroup()
    task_info = ''
    async with state.proxy() as data:
        pass
    tasks = data['tasks']
    for task in tasks:
        if message.text == task:
            task_info, photo_id, document_id = await get_task_info(tasks[task])
            for pic in photo_id:
                media_group.attach(({"media": pic[0][2:-1], "type": 'photo'}))
            for doc in document_id:
                await message.answer_document(doc[0])
    if not media_group:
        await message.answer_media_group(media_group)
    await message.answer(text=task_info, reply_markup=stud_kb())
    await StudentStates.student.set()


# DELETE SUBJECT CHOOSE
@dp.message_handler(Text(equals=subject_delete_str, ignore_case=True), state=StudentStates.student)
async def delete_subject_choose(message: types.Message, state: FSMContext):
    subjects = await get_subjects(message)
    async with state.proxy() as data:
        data['subjects'] = subjects
    markup = createButtons(subjects)
    await message.answer('Выберите предмет который хотите удалить. Имейте ввиду что все задания которые прикреплены '
                         'к предмету тоже будут удалены... (или нет)', reply_markup=markup)
    await DeleteSubject.question.set()


# DELETE SUBJECT CANCEL
@dp.message_handler(Text(equals=cancel_str, ignore_case=True), state=DeleteSubject.question)
async def delete_subject_cancel(message: types.Message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=stud_kb())
    await state.reset_data()
    await StudentStates.student.set()


# DELETE SUBJECT QUESTION
@dp.message_handler(state=DeleteSubject.question)
async def delete_subject_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    if message.text in data['subjects']:
        await message.answer('Вы действительно хотите удалить данный предмет?', reply_markup=question_kb)
        await DeleteSubject.next()


# DELETE SUBJECT YES
@dp.message_handler(Text(equals=yes_str, ignore_case=True), state=DeleteSubject.confirm)
async def delete_subject_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    await message.answer('Идет процесс удаления предмета')
    if not await deleteSubject(message, data['subject']):
        await message.answer('Предмет удален')
    else:
        await message.answer('Что-то пошло не так, предмет не удалился')
    await state.reset_data()
    await StudentStates.student.set()


# DELETE SUBJECT NO
@dp.message_handler(Text(equals=no_str, ignore_case=True), state=DeleteSubject.question)
async def delete_subject_no(message: types.Message, state: FSMContext):
    if message.text in (await state.get_data()):
        await message.answer('Вы действительно хотите удалить данный предмет?', reply_markup=question_kb)
        await DeleteSubject.question.set()


# ADD SUBJECT NAME
@dp.message_handler(Text(equals=subject_add_str, ignore_case=True), state=StudentStates.student)
async def add_subject_name(message: types.Message, state: FSMContext):
    await message.answer('Для добавления нового предмета, дайте ему название', reply_markup=cancel_kb)
    await AddSubject.add.set()


# ADD SUBJECT CANCEL
@dp.message_handler(Text(equals=subject_add_str, ignore_case=True), state=StudentStates.student)
async def add_subject_cancel(message: types.Message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=stud_kb())
    await StudentStates.student.set()


# ADD SUBJECT ADD IN DB
@dp.message_handler(state=AddSubject.add)
async def add_subject_name(message: types.Message, state: FSMContext):
    await message.answer('Идет процесс добавления предмета...', reply_markup=cancel_kb)
    info = await Student.filter(chat_id=message.chat.id).select_related('group')
    info = info[0]
    await Subject(name=message.text,
                  user_id=info.id,
                  group_id=info.group_id,
                  date_creation=datetime.now().strftime('%Y-%m-%d')).save()
    await message.answer('Предмет добавился', reply_markup=stud_kb())
    await StudentStates.student.set()


# CONFIGURE SUBJECTS
@dp.message_handler(Text(equals=configure_subject_str), state=StudentStates.student)
async def configure_subjects(message: types.Message, state: FSMContext):
    await message.answer('Настройка предметов', reply_markup=subject_kb)


'''
# UPLOAD DOCUMENT
    @dp.message_handler(content_types=['document'], state=StudentStates.student)
    async def upload_document(message: types.Message, state: FSMContext):
        hash = await keep_document(message)
        await save_document(hash, task)
        await message.answer('Документ был загружен', reply_markup=subject_kb)
'''
