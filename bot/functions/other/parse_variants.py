import re

a = '1-12 1 2 3 4'
b = '-1-40 1 2 3'
c = '30 - 39 31'
d = '1 - 30 90 91 1 2 3'


def parse_variant(msg):
    var_start, var_end, var_exclude = 0, 0, []
    all_parts = re.findall(r'^(\d{1,6})[- ]{1,3}(\d{1,6})[ ]{0,3}(.*)?$', msg)
    if not all_parts:
        return 1
    all_parts = all_parts[0]
    for i in range(len(all_parts)):
        elem = all_parts[i]
        if not elem.isdigit() and i != 2:
            return 1
        elif i == 2:
            pass
        else:
            elem = int(elem)
        if i == 0:
            if 0 < elem < 999_999:
                var_start = elem
            else:
                return 1
        if i == 1:
            if var_start < elem < 999_999:
                var_end = elem
            else:
                return 1
        if i == 2:
            if elem != '':
                elem = elem.split()
                for j in elem:
                    if j.isdigit():
                        if int(j) < int(var_end):
                            var_exclude.append(str(j))
                        else:
                            return 1
                    else:
                        return 1
                print(var_exclude)
                var_exclude = ' '.join(var_exclude)
            return [var_start, var_end, var_exclude]