import os
import pandas as pd
import numpy as np
import env
import time


def get_read_path():
    return env.ROOT_DIR + 'Origin/'


def get_write_path():
    path = env.ROOT_DIR + '2D/'
    if not os.path.isdir(path):
        os.makedirs(path)

    return path


# エリアと時間別に人数を+1ずつしていく
def distribute_people(base, read):
    """
    :type base: pd.DataFrame
    :type read: pd.DataFrame
    """
    df_new = pd.DataFrame()

    # グルーピングすることでforが回る数を減らし高速化
    group_list = read.groupby(['time'])
    for _name, _group in group_list:
        # 同じ時間帯のみコピーで取り出す
        tmp = base.loc[base['time'] == _name].copy()
        for g in np.asanyarray(_group):
            # {id, type, is_arrived, time, road, x, y, area}
            # 3はtime, 7はarea
            tmp.loc[tmp['area'] == g[7], 'people'] += 1
        df_new = pd.concat([df_new, tmp])

    return df_new


# 出力するフォーマットのベースを作る
def create_people_dataframe():
    times_length = 6
    area_length = 36

    people_dataframe = np.zeros((times_length * area_length, 3))
    people_dataframe = pd.DataFrame(people_dataframe, columns=['time', 'area', 'people'])

    index = 0
    for time in range(times_length):
        for area in range(area_length):
            people_dataframe.loc[index, ['time', 'area']] = [[3600 * (time + 1), area]]
            index += 1

    return people_dataframe


if __name__ == '__main__':
    df_base = create_people_dataframe()

    dir_list = ['people10000', 'people20000', 'people30000']
    csv_list = ['census', 'mobile']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT)]

    for _dir in dir_list:
        for _seed in seed_list:
            for _csv in csv_list:
                df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv',
                                      encoding='Shift_JISx0213',
                                      dtype=None,
                                      delimiter=',')

                start = time.time()

                output = distribute_people(df_base.copy(), df_read)
                output.to_csv(get_write_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv')
                print(_dir + 'seed' + _seed + _csv + '.csv')

                elapsed_time = time.time() - start
                print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
