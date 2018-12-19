import os
import pandas as pd
import numpy as np
import env


def get_read_path():
    return env.ROOT_DIR() + '2D/'


def get_write_path():
    path = env.ROOT_DIR() + '3D/'
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
        tmp = base.loc[:, _name].copy()
        # print(_group)
        # print(tmp)
        for index, value in enumerate(np.asanyarray(_group)):
            # print(value)
            tmp[index] = value[2]
        df_new = pd.concat([df_new, tmp], axis=1)

    return df_new


def create_people_dataframe():
    return pd.DataFrame(np.zeros((36, 6)), columns=[3600 * (i + 1) for i in range(6)])


if __name__ == '__main__':
    df_base = create_people_dataframe()

    dir_list = ['people10000', 'people20000', 'people30000']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT())]
    csv_list = ['census', 'mobile']

    for _dir in dir_list:
        for _seed in seed_list:
            for _csv in csv_list:
                df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv', index_col=0)
                output = distribute_people(df_base.copy(), df_read)
                output.to_csv(get_write_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv')
                print(_dir + 'seed' + _seed + _csv + '.csv')


