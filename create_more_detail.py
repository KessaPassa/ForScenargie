import os
import pandas as pd
import numpy as np
import seaborn as sns
import math
import time
import env
import warnings
warnings.filterwarnings('ignore')


def get_read_path():
    return env.ROOT_DIR()


def get_write_path():
    path = env.ROOT_DIR() + 'more_detail_2D/'
    if not os.path.isdir(path):
        os.makedirs(path)

    return path


def create_regplot(df, order=3):
    trainX = df['ds'].values.reshape(-1, 1)
    trainY = df['y'].values.reshape(-1, 1)
    Px = np.arange(0, len(trainX), 1)
    try:
        sns.regplot(x=Px, y=trainY, order=order, ci=75)
        z = np.polyfit(Px, trainY, 3)
        z = np.squeeze(z)
        p = np.poly1d(z)
        return p
    except:
        return 0


def culculate_3d_regression(df, x):
    p = create_regplot(df)
    p = np.asanyarray(p)
    try:
        y = p[0] * x ** 3 + p[1] * x ** 2 + p[2] * x + p[3]
        return y
    except:
        return 0


if __name__ == '__main__':
    dir_list = ['people10000', 'people20000', 'people30000']
    seed_list = [str(123 + i) for i in range(3)]
    csv_list = ['census', 'mobile']
    area_list = [str(i) for i in range(env.MAX_AREA_COUNT())]
    times_list = [i + 0.5 for i in range(6)]

    csv_array = {}
    for _dir in dir_list:
        csv_array[_dir] = {}
        for _seed in seed_list:
            csv_array[_dir][_seed] = {}
            for _csv in csv_list:
                csv_array[_dir][_seed][_csv] = {}
                for _area in area_list:
                    df = pd.read_csv(
                        get_read_path() + 'datetime_per_area/' + _dir + 'seed' + _seed + '_' + _csv + _area + '.csv',
                        index_col=0,
                        encoding='Shift_JISx0213')
                    df.reset_index(drop=True, inplace=True)
                    csv_array[_dir][_seed][_csv][_area] = df

    main_array = {}
    for _dir in dir_list:
        main_array[_dir] = {}
        for _seed in seed_list:
            main_array[_dir][_seed] = {}
            for _csv in csv_list:
                df = pd.read_csv(get_read_path() + '2D/' + _dir + 'seed' + _seed + '_' + _csv + '.csv',
                                 encoding='Shift_JISx0213')
                main_array[_dir][_seed][_csv] = df

    print('準備の読み込み終了')

    for _dir in dir_list:
        for _seed in seed_list:
            for _csv in csv_list:
                start = time.time()

                df_array = pd.DataFrame()
                for _area in area_list:
                    for _times in times_list:
                        _people = culculate_3d_regression(csv_array[_dir][_seed][_csv][_area].copy(), _times)
                        _times = int(_times * 3600)
                        tmp = pd.DataFrame([_times, _area, _people], index=['time', 'area', 'people'])
                        tmp = tmp.T
                        df_array = pd.concat([df_array, tmp])
                df = pd.concat([main_array[_dir][_seed][_csv], df_array])
                df[['time', 'area']] = df[['time', 'area']].applymap(lambda x: int(x))
                df['people'] = df['people'].apply(lambda x: 0 if x < 0 else x)
                df['people'] = df['people'].apply(lambda x: math.floor(x))
                df.sort_values(['time', 'area'], inplace=True)
                df.reset_index(drop=True, inplace=True)
                df.to_csv(get_write_path() + _dir + 'seed' + _seed + '_' + _csv + '.csv')
                main_array[_dir][_seed][_csv] = df

                print(_dir + 'seed' + _seed + _csv + '.csv')

                elapsed_time = time.time() - start
                print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
