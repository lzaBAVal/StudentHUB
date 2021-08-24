from prometheus_client import Counter

app_click = Counter('app_click', 'Description of counter')
error_message = Counter('error_message', 'Error message')
db_click = Counter('db_click', 'Database click')
new_user = Counter('new_user', 'Added new user')
trottled = Counter('trottled_clicks', 'Trottled counter')
functions = {}


def prom_app_click():
    app_click.inc()


def prom_group_click(group_id):
    group_click = Counter(f'group_{group_id}', '')
    group_click.inc()


def prom_error():
    error_message.inc()


def prom_handler_click(func):
    if not func in functions:
        functions[f'{func}'] = (Counter(f'function_{func}', ''))
    (functions[f'{func}']).inc()


def prom_db_click():
    db_click.inc()


def prom_new_user():
    new_user.inc()


def prom_thottled():
    trottled.inc()