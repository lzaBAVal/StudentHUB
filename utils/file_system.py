
import os

from old_config import PATH_WIN

PATH = 'C:\\Users\\zaBAVa\\bot_fs'
str_hex = '0123456789abcdef'

if not os.path.isdir(PATH):
    os.mkdir(PATH)
else:
    print('file exist')


# CREATE 256 * 256 FILES. PATH\3a\3a78
def create_system_directory():
    for i in str_hex:
        for j in str_hex:
            for k in str_hex:
                for l in str_hex:
                    os.makedirs(f'{PATH}\\{i}{j}\\{i}{j}{k}{l}')
    print('End')


def create_new_file(f_name: str):
    if len(f_name) != 32:
        return False
    #else:
    #    os.


def get_path(hash_md5):
    layer1 = hash_md5[0:2]
    layer2 = hash_md5[0:4]
    return str(f"{PATH_WIN}{layer1}\\{layer2}\\")
