import os
from collections import namedtuple


def BASE_DIR_NAME():
    return '20190402'


def SCENARGIE_DIR():
    name = BASE_DIR_NAME()
    return 'C:/Users/admin/Documents/Scenargie/{}/Batches/'.format(name)


def ROOT_DIR():
    os_name = os.name

    if os_name == 'posix':
        return '/Users/kessapassa/OneDrive/research_log/' + BASE_DIR_NAME() + '/'
    elif os_name == 'nt':
        return 'C:/Users/admin/OneDrive/research_log/' + BASE_DIR_NAME() + '/'


def DIR_LIST():
    return ['p10000', 'p20000', 'p30000']


def RATIO_LIST():
    return ['r4', 'r5', 'r6']


def MAX_SEED_COUNT():
    return 1


def MAX_AREA_COUNT():
    one_length = 9
    return one_length * one_length


def MAX_TIME_COUNT():
    return 6


# ファイルを読み込むためのfor文で使う引数
ARGS_FOR_LIST = namedtuple('FOR_LIST', ('dir', 'ratio', 'seed', 'csv'))


# ファイル名を作成して返す
def get_file_name(args):
    return args.dir + args.ratio + args.seed + '_' + args.csv + '.csv'


def get_for_list():
    dir_list = DIR_LIST()
    ratio_list = RATIO_LIST()
    seed_list = ['s' + str(123 + i) for i in range(MAX_SEED_COUNT())]
    csv_list = ['census', 'mobile']

    return ARGS_FOR_LIST(dir_list, ratio_list, seed_list, csv_list)


# フォルダにアクセスするたびにこのfor文を使う
def for_default(func):
    for_list = get_for_list()
    for _dir in for_list.dir:
        for _ratio in for_list.ratio:
            for _seed in for_list.seed:
                for _csv in for_list.csv:
                    args = ARGS_FOR_LIST(_dir, _ratio, _seed, _csv)
                    func(args)
