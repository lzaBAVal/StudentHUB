from tmp_files.flexible_time import check_flex_time


def unit_test_check_flex_time():
    for i in range(24):
        for j in range(0, 60, 5):
            for m in range(24):
                for n in range(0, 60, 5):
                    time_string = f'{i}:{j} - {m}:{n}'
                    if check_flex_time(time_string) is True:
                        print(f'{time_string} - {check_flex_time(time_string)}')