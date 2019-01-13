import os


def ROOT_DIR():
    os_name = os.name
    dir_name = '20190113'
    if os_name == 'posix':
        return '/Users/kessapassa/OneDrive/research_log/' + dir_name + '/'
    elif os_name == 'nt':
        return 'C:/Users/admin/OneDrive/research_log/' + dir_name + '/'


def MAX_SEED_COUNT():
    return 3


def MAX_AREA_COUNT():
    return 7 * 7


def MAX_TIME_COUNT():
    return 6
