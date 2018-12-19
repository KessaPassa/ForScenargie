import os
import numpy as np
import pandas as pd
import env
import time


def get_read_path():
    return env.ROOT_DIR() + 'Origin/'


def get_write_path():
    path = env.ROOT_DIR() + 'OD/'
    if not os.path.isdir(path):
        os.makedirs(path)

    return path


# 時間のindexとリストを返す
def split_type(time):
    times_list = [3600 * (i + 1) for i in range(6)]
    index = times_list.index(time)
    for key, value in enumerate(times_list):
        if key == index:
            pass
        else:
            times_list[key] = np.nan
    # print(times_list)
    return index, times_list


# idを元に時間別所在エリアを記述
def distribute_od(base, read):
    """
    :type base: pd.DataFrame
    :type read: pd.DataFrame
    """
    for value in np.asanyarray(read):
        # value = ['id', 'type', 'time', 'area']
        row = base.loc[base['id'] == value[0]]

        # もし空なら新しく行を作成し、追加
        # row.empty
        if len(row.index) == 0:
            columns_list = [value[0], value[1]]
            index, times_list = split_type(value[2])
            times_list[index] = value[3]
            columns_list.extend(times_list)

            tmp = pd.Series(columns_list, index=base.columns)
            base = base.append(tmp, ignore_index=True)

        # 既に同じIDがあるなら時間帯のエリアを追加
        else:
            base.loc[row.index, ['type', value[2]]] = [value[1], value[3]]

    return base


# 出力元となるdataframeの雛形
def create_base_dataframe():
    times_list = [3600 * (i + 1) for i in range(6)]
    columns = ['id', 'type']
    columns.extend(times_list)

    df = pd.DataFrame(columns=columns)
    return df


if __name__ == '__main__':
    df_base = create_base_dataframe()
    dir_list = ['people10000', 'people20000', 'people30000']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT())]
    csv_list = ['mobile']

    for _dir in dir_list:
        for _seed in seed_list:
            for _csv in csv_list:
                df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv',
                                      encoding='Shift_JISx0213')

                start = time.time()

                df_read = df_read.loc[:, ['id', 'type', 'time', 'area']]
                output = distribute_od(df_base.copy(), df_read)
                output.to_csv(get_write_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv',
                              index=False)
                print(_dir + 'seed' + _seed + _csv + '.csv')

                elapsed_time = time.time() - start
                print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
