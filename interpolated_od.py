import os
import pandas as pd
import numpy as np
import env


def get_read_path():
    return env.ROOT_DIR() + 'OD/'


def get_write_path():
    path = env.ROOT_DIR() + 'Interpolated_OD/'
    if not os.path.isdir(path):
        os.makedirs(path)

    return path


# NaNではない最初の値のindexを返す
def find_not_nan_index(_list):
    for key, value in enumerate(_list):
        if not np.isnan(value):
            return key

    return -1


# NaNになっている時間を補間する
def interpolate_times(df):
    new_times = []
    for value in np.asanyarray(df):
        times = value[2:]

        # 最初の取得時間3600がNaNなら出現していないので、自宅に居た体で補間
        if np.isnan(times[0]):
            index = find_not_nan_index(times)
            for i in range(index):
                times[i] = times[index]

        # is_arrived == Trueなら目的地に着いて消えてるので、遊んでいる体で補間
        if np.isnan(times[5]):
            times = times[::-1]
            index = find_not_nan_index(times)
            for i in range(index):
                times[i] = times[index]
            times = times[::-1]

        new_times.append(np.concatenate([value[:2], times]))

    times_list = [str(3600 * (i + 1)) for i in range(6)]
    columns = ['id', 'type'].extend(times_list)
    df_new = pd.DataFrame(new_times, columns=columns)
    return df_new


if __name__ == '__main__':
    dir_list = env.DIR_LIST()
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT())]
    csv_list = ['mobile']

    for _dir in dir_list:
        for _seed in seed_list:
            for _csv in csv_list:
                df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv',
                                      encoding='Shift_JISx0213')
                output = interpolate_times(df_read)
                output.to_csv(get_write_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv',
                              index=False)
                print(_dir + 'seed' + _seed + _csv + '.csv')
