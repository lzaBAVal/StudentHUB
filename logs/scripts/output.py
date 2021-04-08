import os
import re
import shutil
from logs.scripts.logging_core import init_logger

logger = init_logger()
out_log = 'logs/out_log.log'
core_log = 'logs/core.log'


def get_last_logs():
    if harvest_logs() == -1:
        return -1
    old_result = ''
    additional_lines = 5
    result = ''
    for iter in range(10):
        result = ''
        file = open(out_log, 'r')
        linelist = file.readlines()
        file.close()
        for i in reversed(range(1, 5 + additional_lines*iter)):
            result += linelist[i]
        if len(result) > 3000:
            return old_result
        elif 3000 > len(result) > 2800 or 5 + additional_lines*iter >= len(linelist) - 7:
            return result
        else:
            old_result = result
    return result


def get_user_logs(id_chat):
    pass


def divide_logs_by_levels():
    pass


def harvest_logs():
    try:
        if os.stat(f'{core_log}'):
            shutil.copy(f'{core_log}', f'{out_log}')
    except FileNotFoundError as exc:
        logger.exception(exc)
        return -1


def get_last_critical_logs():
    if harvest_logs() == -1:
        return -1
    file = open(out_log, 'r')
    flag, counter = 0, 0
    strings = []
    result = ''
    for i in file:
        if(re.match(r'^\[\d{4}-\d{1,2}-\d{1,2} .*:.*:\d+:(ERROR|WARNING|CRITICAL).*\]', i)):
            if counter >= 3:
                result += strings[-2] + '\n' + strings[-1] + '\n'
            flag = 1
            result += '\n' + i
            counter = 0
        elif not (re.match(r'^\[\d{4}-\d{1,2}-\d{1,2} .*:.*:\d+:(DEBUG|INFO|).*\]', i)) and flag == 1:
            if counter <= 2:
                result += i
            strings.append(i)
            counter += 1
        else:
            flag = 0

    return result
