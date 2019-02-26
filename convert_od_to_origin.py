import os
import numpy as np
import pandas as pd
import env


def get_read_path():
    return env.ROOT_DIR() + 'Interpolated_OD/'


def get_write_path():
    path = env.ROOT_DIR() + 'Interpolated_Origin/'
    if not os.path.isdir(path):
        os.makedirs(path)

    return path


def split_per_time(read):
    array = []
    for row in np.asanyarray(read):
        for i in range(6):
            array.append([row[0], row[1], str(3600 * (i + 1)), row[2 + i]])
    df_new = pd.DataFrame(array, columns=['id', 'type', 'time', 'area'])

    return df_new


if __name__ == '__main__':
    dir_list = env.DIR_LIST()
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT())]

    for _dir in dir_list:
        for _seed in seed_list:
            csv_name = 'mobile'
            df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '_' + csv_name + '.csv')
            output = split_per_time(df_read)
            output.to_csv(get_write_path() + _dir + 'seed' + _seed + '_' + csv_name + '.csv',
                          index=False)
            print(_dir + 'seed' + _seed + csv_name + '.csv')

            # censusも同じディレクトリの方が都合が良いので抽出して出力する
            csv_name = 'census'
            df_read = pd.read_csv(env.ROOT_DIR() + 'Origin/' + _dir + 'seed' + _seed + '_' + csv_name + '.csv',
                                  encoding='Shift_JISx0213')
            output = df_read.loc[:, ['id', 'type', 'time', 'area']]
            output.to_csv(get_write_path() + _dir + 'seed' + _seed + '_' + csv_name + '.csv',
                          index=False)
            print(_dir + 'seed' + _seed + csv_name + '.csv')
