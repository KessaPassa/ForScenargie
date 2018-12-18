import os
import pandas as pd
import numpy as np
import env
import time


def get_read_path():
    return env.ROOT_DIR + '2D/'


def get_write_path():
    path = env.ROOT_DIR + '3D/'
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
        print(_group)
        for g in np.asanyarray(_group):
            # {id, type, is_arrived, time, road, x, y, area}
            # 3はtime, 7はarea
            tmp.loc[tmp['area'] == g[1], 'people'] += g[2]
        df_new = pd.concat([df_new, tmp])

    return df_new


def create_people_dataframe():
    return pd.DataFrame(np.zeros((36, 6)), columns=[3600 * (i + 1) for i in range(6)])


if __name__ == '__main__':
    df_base = create_people_dataframe()

    dir_list = ['people10000', 'people20000', 'people30000']
    csv_list = ['census', 'mobile']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT)]

    for _dir in dir_list:
        for _seed in seed_list:
            for _csv in csv_list:
                print(get_read_path())
                df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv')
                output = distribute_people(df_base, df_read)


