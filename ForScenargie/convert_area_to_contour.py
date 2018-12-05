import numpy as np
import pandas as pd
import env



def get_read_path():
    return env.ROOT_DIR + 'Origin/'


def get_write_path():
    return env.ROOT_DIR + ''


# エリア番号を線形的な数から、iとjで回した数のようにする
def convert_area_to_contour(area_id):
    area_id = int(area_id)
    contour_id = str(area_id // 6)
    contour_id += str(area_id % 6) + '0'

    return contour_id


# エリア番号を線形的な数から、iとjで回した数のようにする
if __name__ == '__main__':
    dir_list = ['2_8', '4_6', '6_4', '8_2']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT)]
    times_list = [str(3600 * (i + 1)) for i in range(6)]

    for _dir in dir_list:
        for _seed in seed_list:
            df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '.csv',
                                  encoding='Shift_JISx0213')
            df_read[times_list] = df_read[times_list].apply(convert_area_to_contour)
            df_read.to_csv(get_write_path() + _dir + 'seed' + _seed + '.csv')
