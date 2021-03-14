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
