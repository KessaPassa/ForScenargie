import os


def SCENARGIE_DIR():
    return 'C:/Users/admin/Documents/Scenargie/20190331/Batches/'


def OUTPUT_DIR_NAME():
    return '20190331'


def ROOT_DIR():
    os_name = os.name

    if os_name == 'posix':
        return '/Users/kessapassa/OneDrive/research_log/' + OUTPUT_DIR_NAME() + '/'
    elif os_name == 'nt':
        return 'C:/Users/admin/OneDrive/research_log/' + OUTPUT_DIR_NAME() + '/'


def DIR_LIST():
    return ['p10000', 'p20000', 'p30000']


def RATIO_LIST():
    return ['r6', 'r5', 'r4']


def MAX_SEED_COUNT():
    return 1


def MAX_AREA_COUNT():
    one_length = 9
    return one_length * one_length


def MAX_TIME_COUNT():
    return 6
