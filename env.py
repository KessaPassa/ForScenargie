import os


def SCENARGIE_DIR():
    return 'C:/Users/admin/Documents/Scenargie/2018_Graduate/case/'


def ROOT_DIR():
    os_name = os.name
    dir_name = '20190114'
    if os_name == 'posix':
        return '/Users/kessapassa/OneDrive/research_log/' + dir_name + '/'
    elif os_name == 'nt':
        return 'C:/Users/admin/OneDrive/research_log/' + dir_name + '/'


def MAX_SEED_COUNT():
    return 3


def MAX_AREA_COUNT():
    one_length = 9
    return one_length * one_length


def MAX_TIME_COUNT():
    return 6
