import openpyxl as px
import pandas as pd
import csv
from enum import Enum
import secrets


class Axis(Enum):
    id = 0
    type = 1
    time = 2
    road = 3
    x = 4
    y = 5
    area = 6


READ_FILE_NAME = '_ConvertPosToArea'
WRITE_FILE_NAME = 'all_vehicle'


# AXIS_LENGTH = 7
# FILE_COUNT = 10
# START_NUMBER = 123
# MAX_AREA_COUNT = 25
# MAX_TIME_COUNT = 6


# ファイルパスを返す
def getFilePath(seed=-1, plusname=''):
    if seed == -1:
        return secrets.DIRECTRY_PATH + secrets.DIRECTRY_NAME + '/'
    else:
        return secrets.DIRECTRY_PATH + secrets.DIRECTRY_NAME + '/seed' + str(secrets.START_NUMBER + seed) + plusname


# CSVからExcelへ変換
# パス名は英語のみ
def convertCsvToExcel(name):
    # CSVファイルの読み込み
    data = pd.read_csv(name + '.csv', encoding='shift-jis')
    # Excel形式で出力
    data.to_excel(name + '.xlsx', encoding='shift-jis', header=None, index=None)

    return name + '.xlsx'


def getRow(file):
    reader = csv.reader(file, delimiter=',')
    for rows in reader:
        row = csv.reader(rows, delimiter=',')

        buf = []
        for index, cells in enumerate(row):
            # for num in range(AXIS_LENGTH):
            cell = str(cells).split("'")

            if index in {Axis.id.value, Axis.time.value, Axis.area.value}:
                buf.append(int(cell[1]))
            elif index in {Axis.x.value, Axis.y.value}:
                buf.append(float(cell[1]))
            else:
                buf.append(str(cell[1]))

        ws.append(buf)


if __name__ == '__main__':
    wb = px.Workbook()
    ws = wb.active

    for seed in range(secrets.FILE_COUNT):
        ws = wb.create_sheet(title='seed' + str(secrets.START_NUMBER + seed))
        file = open(getFilePath(seed, READ_FILE_NAME) + '.csv')
        getRow(file)
        file.close()

    wb.save(getFilePath() + WRITE_FILE_NAME + '.xlsx')
