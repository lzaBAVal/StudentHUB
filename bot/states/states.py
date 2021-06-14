from aiogram.dispatcher.filters.state import State, StatesGroup

'''
class TestStates(Helper):
    mode = HelperMode.snake_case

    TEST_STATE_0 = ListItem()
    TEST_STATE_1 = ListItem()
    TEST_STATE_2 = ListItem()
    TEST_STATE_3 = ListItem()
    TEST_STATE_4 = ListItem()
    TEST_STATE_5 = ListItem()
'''


class TesterState(StatesGroup):
    tester = State()
    start_add = State()
    finish_add = State()


class AnonStates(StatesGroup):
    anon = State()


class StudentStates(StatesGroup):
    student = State()
    captain = State()


class RegistrationStates(StatesGroup):
    name = State()
    surname = State()
    find_group = State()
    accept_all_data = State()
    insert_sql = State()
    final = State()


class AddLesson(StatesGroup):
    time = State()
    lesson = State()
    teacher = State()
    subgroup = State()
    classroom = State()
    check = State()
    process = State()
    final = State()


class DeleteLesson(StatesGroup):
    lesson = State()
    check = State()
    process = State()
    final = State()


class DiscoverFreeTime(StatesGroup):
    output = State()


class Calculate(StatesGroup):
    score = State()


class AdminCheckUser(StatesGroup):
    user_id = State()
    output = State()


class AdminBanUser(StatesGroup):
    user_id = State()


class AdminUnbanUser(StatesGroup):
    user_id = State()


class AdminGiveRights(StatesGroup):
    user_id = State()
    issue = State()


class AdminTakeAwayRights(StatesGroup):
    user_id = State()
    issue = State()


class CaptainSchedule(StatesGroup):
    select = State()


class ConfigWhoseScheduleState(StatesGroup):
    select = State()


class SetCaptainState(StatesGroup):
    set = State()


class AdminPrintArhit(StatesGroup):
    select = State()


class CreateNewTask(StatesGroup):
    # Object
    name = State()
    description = State()
    variants = State()
    photo_start = State()
    photo_upload = State()
    check_question = State()
    End = State()
    create_subject = State()


class DeleteTask(StatesGroup):
    question = State()
    confirm = State()


class ShowTask(StatesGroup):
    choose = State()


class ConfigureScheduleParts(StatesGroup):
    # menu
    choose_part = State()


class DeleteSubject(StatesGroup):
    # choose_object = State()
    question = State()
    confirm = State()


class AddSubject(StatesGroup):
    add = State()
