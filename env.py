import os
import time
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


# フォルダのチェック。すでにあるということは上書きの危険があるため
def check_write_dir(name):
    path = ROOT_DIR() + name + '/'
    if os.path.isdir(path):
        print('指定フォルダ [{}] は既に存在します'.format(path))
        print('上書き処理しますか？(y/n)')
        command = input()
        if not command == 'y':
            return False
    else:
        os.makedirs(path)
        print('{} にフォルダを作成しました'.format(path))

    return True


def get_read_path(name):
    path = ROOT_DIR() + name + '/'
    return path


# ファイル名を作成して返す
def get_file_name(args, any=None):
    if any is None:
        return args.dir + args.ratio + args.seed + '_' + args.csv + '.csv'
    else:
        return args.dir + args.ratio + args.seed + '_' + args.csv + any + '.csv'


def get_full_path(name, args, any=None):
    return get_read_path(name) + get_file_name(args, any)


def get_col_names():
    col_names = ['c{0:02d}'.format(i) for i in range(30)]
    return col_names


def get_times_list():
    times_list = [str(3600 * (i + 1)) for i in range(MAX_TIME_COUNT())]
    return times_list


def get_area_list():
    area_list = [str(i) for i in range(MAX_AREA_COUNT())]
    return area_list


def get_for_list():
    dir_list = DIR_LIST()
    ratio_list = RATIO_LIST()
    seed_list = ['s' + str(123 + i) for i in range(MAX_SEED_COUNT())]
    csv_list = ['census', 'mobile']

    return ARGS_FOR_LIST(dir_list, ratio_list, seed_list, csv_list)


def for_default_init(func, array):
    start_sum = time.time()
    for_list = get_for_list()

    for _dir in for_list.dir:
        array[_dir] = {}

        for _ratio in for_list.ratio:
            array[_dir][_ratio] = {}

            for _seed in for_list.seed:
                array[_dir][_ratio][_seed] = {}

                for _csv in for_list.csv:
                    array[_dir][_ratio][_seed][_csv] = {}
                    args = ARGS_FOR_LIST(_dir, _ratio, _seed, _csv)

                    start = time.time()
                    func(args, array)
                    print(get_file_name(args))
                    print('elapsed_time:{0}'.format(time.time() - start) + '[sec]')
    print('¥n' + 'sum_time:{0}'.format(time.time() - start_sum) + '[sec]')


# フォルダにアクセスするたびにこのfor文を使う
def for_default(func):
    start_sum = time.time()
    for_list = get_for_list()
    for _dir in for_list.dir:
        for _ratio in for_list.ratio:
            for _seed in for_list.seed:
                for _csv in for_list.csv:
                    args = ARGS_FOR_LIST(_dir, _ratio, _seed, _csv)

                    start = time.time()
                    func(args)
                    print(get_file_name(args))
                    print("elapsed_time:{0}".format(time.time() - start) + "[sec]")
    print('¥n' + "sum_time:{0}".format(time.time() - start_sum) + "[sec]")
