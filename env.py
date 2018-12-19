import os


def ROOT_DIR():
    os_name = os.name
    if os_name == 'posix':
        return '/Users/kessapassa/OneDrive/research_log/2018_Graduate/'
    elif os_name == 'nt':
        return 'C:/Users/admin/OneDrive/research_log/2018_Graduate/'


def MAX_SEED_COUNT():
    return 3
