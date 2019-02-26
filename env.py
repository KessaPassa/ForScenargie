import os


def SCENARGIE_DIR():
    return 'C:/Users/admin/Documents/Scenargie/20190226/Batches/movement_cross_'


def ROOT_DIR():
    os_name = os.name
    dir_name = '20190226'
    if os_name == 'posix':
        return '/Users/kessapassa/OneDrive/research_log/' + dir_name + '/'
    elif os_name == 'nt':
        return 'C:/Users/admin/OneDrive/research_log/' + dir_name + '/'

def DIR_LIST():
    return ['people30000']


def MAX_SEED_COUNT():
    return 1


def MAX_AREA_COUNT():
    one_length = 9
    return one_length * one_length


def MAX_TIME_COUNT():
    return 6
