import os
import pandas as pd
import numpy as np
import shutil
import env

CHILD_DIR = 'mobility-seed_'

TIME_PER_SPLIT = 3600

X_ZERO_AREA_POS = -10700
Y_ZERO_AREA_POS = -11250
AREA_RANGE = 2000
RADIUS = AREA_RANGE / 2

# class Areaを格納する配列
area = []


class Area:
    id = -1
    x = -1
    y = -1

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    @property
    def get_id(self):
        return self.id

    @property
    def get_x(self):
        return self.x

    @property
    def get_y(self):
        return self.y


# ファイルパスを返す
def get_read_path(_dir, _seed, _csv):
    return env.SCENARGIE_DIR() + _dir + '/' + '10_0' + '/' + CHILD_DIR + _seed + '/' + _csv + '.csv'


def get_write_path(name):
    path = env.ROOT_DIR() + name + '/'
    if not os.path.isdir(path):
        os.makedirs(path)

    return path


# area0を左下起点にメッシュ範囲を作成
def make_area_mesh():
    one_side = np.sqrt(env.MAX_AREA_COUNT())
    for index in range(env.MAX_AREA_COUNT()):
        x = X_ZERO_AREA_POS + AREA_RANGE * (index % one_side)
        y = Y_ZERO_AREA_POS + AREA_RANGE * (index // one_side)
        area.append(Area(index, x, y))
        # print(vars(area[index]))


# 到着時間も含まれているので1時間ごとの時間に補間する
def interpolate_time(time):
    times_list = [3600 * (i + 1) for i in range(env.MAX_TIME_COUNT())]
    times = []

    if time in times_list:
        times = time
    elif 0 < time < times_list[0]:
        times = times_list[0]
    elif times_list[0] < time < times_list[1]:
        times = times_list[1]
    elif times_list[1] < time < times_list[2]:
        times = times_list[2]
    elif times_list[2] < time < times_list[3]:
        times = times_list[3]
    elif times_list[3] < time < times_list[4]:
        times = times_list[4]
    elif times_list[4] < time < times_list[5]:
        times = times_list[5]

    return pd.Series(times)


# 新しく作成したareaカラムにメッシュ番号を入力する
def set_area_id(df):
    """
    :type df: pd.DataFrame
    """
    df['area'] = -1
    for index in range(env.MAX_AREA_COUNT()):
        df.loc[
            (area[index].get_x - RADIUS <= df['x']) & (df['x'] <= area[index].get_x + RADIUS) &
            (area[index].get_y - RADIUS <= df['y']) & (df['y'] <= area[index].get_y + RADIUS),
            'area'] = area[index].get_id


# Scenargieのoutput dataがあるPCで実行すること
if __name__ == '__main__':
    make_area_mesh()

    columns = ['id', 'type', 'is_arrived', 'time', 'road', 'x', 'y']
    dir_list = ['people10000', 'people20000', 'people30000']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT())]
    csv_list = ['census', 'mobile']

    for _dir in dir_list:
        for _seed in seed_list:
            for _csv in csv_list:
                # ただのshift-jisではダメ
                df = pd.read_csv(get_read_path(_dir, _seed, _csv), names=columns, encoding='Shift_JISx0213')

                # 上書きしないようにコピーする
                reader = df.copy()

                # 新しくarea列を追加
                set_area_id(reader)

                # road列から(census)を取り除く
                reader['road'] = reader['road'].apply(lambda x: x.split('(census)')[0])

                # time列を補間
                reader['time'] = reader['time'].apply(interpolate_time)

                # od to area用に-1を除かないモノも保存する
                if _csv == 'census':
                    reader.to_csv(get_write_path('include_area_-1') + _dir + 'seed' + _seed + '_' + _csv + '.csv',
                                  index=None,
                                  encoding='Shift_JISx0213')

                # メッシュ番号が-1以外、つまり範囲外の行を削除(範囲内のみ抽出)
                reader = reader[reader['area'] != -1]

                reader.to_csv(get_write_path('Origin') + _dir + 'seed' + _seed + '_' + _csv + '.csv',
                              index=None,
                              encoding='Shift_JISx0213')
                print(_dir + 'seed' + _seed + '_' + _csv + '.csv')

            # od.csvはコピーでOneDriveへ移動
            shutil.copyfile(get_read_path(_dir, _seed, 'od'), get_write_path('Origin') + _dir + 'seed' + _seed + '_' + 'od.csv')
