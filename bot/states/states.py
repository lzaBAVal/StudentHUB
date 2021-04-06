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
    process= State()
    final = State()

class DeleteLesson(StatesGroup):
    lesson = State()
    check = State()
    process = State()
    final = State()

class DiscoverFreeTime(StatesGroup):
    output = State()

class AdminCheckUser(StatesGroup):
    user_id = State()
    output = State()

class AdminGiveRights(StatesGroup):
    user_id = State()
    issue = State()

class AdminTakeAwayRights(StatesGroup):
    user_id = State()
    issue = State()

class CaptainSchedule():
    select = State()