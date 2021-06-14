import os
import re
import shutil
from utils.log.logging_core import init_logger

logger = init_logger()
out_log = 'logs/out_log.log'
core_log = 'logs/core.log'


def get_last_logs():
    if harvest_logs() == -1:
        return -1
    old_result = ''
    additional_lines = 5
    result = ''
    file = open(out_log, 'r')
    linelist = file.readlines()
    file.close()
    linelist = list(reversed(linelist))
    for iteration in range(10):
        for i in reversed(range(additional_lines * iteration, 5 + additional_lines * iteration)):
            result += linelist[i]
        if len(result) > 3000:
            return old_result
        elif 3000 > len(result) > 2800 or 5 + additional_lines * iteration >= len(linelist) - 7:
            return result
        else:
            old_result = result
    return result


def get_user_logs():
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
    result = ''
    old_result = ''
    flag = 0
    counter = 0
    additional_lines = 5
    strings = []
    file = open(out_log, 'r')
    linelist = file.readlines()
    file.close()
    linelist = list(reversed(linelist))
    for iteration in range(30):
        for i in reversed(range(additional_lines * iteration, 5 + additional_lines * iteration)):
            if re.match(r'^\[\d{4}-\d{1,2}-\d{1,2} .*:.*:\d+:(ERROR|WARNING|CRITICAL).*\]', linelist[i]):
                if counter >= 3:
                    result += strings[-2] + '\n' + strings[-1] + '\n'
                flag = 1
                result += '\n' + i
                counter = 0
            elif not (re.match(r'^\[\d{4}-\d{1,2}-\d{1,2} .*:.*:\d+:(DEBUG|INFO|).*\]', i)) and flag == 1:
                if counter <= 2:
                    result += linelist[i]
                strings.append(i)
                counter += 1
            else:
                flag = 0
        if len(result) > 3000:
            return old_result
        elif 3000 > len(result) > 2800 or 5 + additional_lines * iter >= len(linelist) - 7:
            return result
        else:
            old_result = result
    return result
