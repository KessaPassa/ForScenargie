import os


def ROOT_DIR():
    os_name = os.name
    if os_name == 'posix':
        return '/Users/kessapassa/OneDrive/research_log/20181227/'
    elif os_name == 'nt':
        return 'C:/Users/admin/OneDrive/research_log/20181227/'


def MAX_SEED_COUNT():
    return 2
