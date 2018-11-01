import pandas as pd
import numpy as np
import openpyxl as px


READ_DIR_PATH = 'C:/Users/admin/Documents/Scenargie/2018_IWIN/case/'
WRITE_DIR_PATH = 'C:/Users/admin/Documents/Scenargie/2018_IWIN/case/'
READ_FILE_NAME = '_ConvertPosToArea'
WRITE_FILE_NAME = 'all_vehicle'

AXIS_LENGTH = 7
FILE_COUNT = 10
START_NUMBER = 123
MAX_AREA_COUNT = 25
MAX_TIME_COUNT = 6

ROOT_DIR_NAME = 'map1_add_census'
DIR_LIST = ['2_8', '4_6', '6_4', '8_2']
CHILD_DIR = 'mobility-seed_'
CSV_FILE_NAME = 'log.csv'


# ファイルパスを返す
def getReadFilePath(dir_list, seed):
    return READ_DIR_PATH + ROOT_DIR_NAME + '/' + dir_list + '/' + CHILD_DIR + str(seed) + '/' + CSV_FILE_NAME


def getWriteFilePath():
    return WRITE_DIR_PATH + ROOT_DIR_NAME + '/'


if __name__ == '__main__':
    wb = px.Workbook()
    ws = wb.activegit

    for dir_list in DIR_LIST:
        for seed in range(123, 132 + 1):
            tmp = pd.read_csv(getReadFilePath(dir_list, seed), encoding='Shift_JISx0213')

            # 上書きしないようにコピーする
            reader = tmp.copy()
            reader.to_csv(getWriteFilePath() + 'logs/' + dir_list + '_' + 'seed' + str(seed) + '.csv')





