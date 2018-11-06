import pandas as pd
import numpy as np
import openpyxl as px

READ_DIR_PATH = 'C:/Users/admin/Documents/Scenargie/2018_IWIN/case/'
WRITE_DIR_PATH = 'C:/Users/admin/Documents/Scenargie/2018_IWIN/case/'

ROOT_DIR_NAME = 'map1_add_census'
DIR_LIST = ['2_8', '4_6', '6_4', '8_2']
CHILD_DIR = 'mobility-seed_'
CSV_FILE_NAME = 'log.csv'

MAX_AREA_COUNT = 36
MAX_TIME_COUNT = 6
TIME_PER_SPLIT = 3600
COLUMNS = ['id', 'type', 'time', 'road', 'x', 'y']

X_ZERO_AREA_POS = -8700
Y_ZERO_AREA_POS = -9250
# ZERO_MESH_POS = (-8700, -9250)
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
def get_read_file_path(dir_list, seed):
    return READ_DIR_PATH + ROOT_DIR_NAME + '/' + dir_list + '/' + CHILD_DIR + str(seed) + '/' + CSV_FILE_NAME


def get_write_file_path():
    return WRITE_DIR_PATH + ROOT_DIR_NAME + '/'


# area0を左下起点にメッシュ範囲を作成
def make_area_mesh():
    one_side = np.sqrt(MAX_AREA_COUNT)
    for index in range(MAX_AREA_COUNT):
        x = X_ZERO_AREA_POS + AREA_RANGE * (index % one_side)
        y = Y_ZERO_AREA_POS + AREA_RANGE * (index // one_side)
        area.append(Area(index, x, y))
        # print(vars(area[index]))


# 新しく作成したareaカラムにメッシュ番号を入力する
def set_area_id(df):
    """
    :type df: pd.DataFrame
    """
    df['area'] = -1
    for index in range(MAX_AREA_COUNT):
        df.loc[
            (area[index].get_x - RADIUS <= df['x']) & (df['x'] <= area[index].get_x + RADIUS) &
            (area[index].get_y - RADIUS <= df['y']) & (df['y'] <= area[index].get_y + RADIUS),
            'area'] = area[index].get_id


if __name__ == '__main__':
    wb = px.Workbook()
    ws = wb.active

    make_area_mesh()

    for dir_list in DIR_LIST:
        for seed in range(123, 132 + 1):
            # ただのshift-jisではダメ
            tmp = pd.read_csv(get_read_file_path(dir_list, seed), names=COLUMNS, encoding='Shift_JISx0213')

            # 上書きしないようにコピーする
            reader = tmp.copy()
            # 新しくarea列を追加
            set_area_id(reader)

            # メッシュ番号が-1以外、つまり範囲外の行を削除(範囲内のみ抽出)
            reader = reader[reader['area'] != -1]
            # 出力 *道路交通センサスにはjupyterで整形するので基本形のみでおけ
            reader.to_csv(get_write_file_path() + 'logs/' + dir_list + '_' + 'seed' + str(seed) + '.csv',
                          index=None,
                          encoding='Shift_JISx0213')


            # # roadにcensusがついている行のみ抽出
            # reader = reader[reader['road'].str.contains('census')]
            # # 道路交通センサス用に出力
            # reader.to_csv(get_write_file_path() + 'logs/census' + dir_list + '_' + 'seed' + str(seed) + '.csv',
            #               index=None,
            #               encoding='Shift_JISx0213')
