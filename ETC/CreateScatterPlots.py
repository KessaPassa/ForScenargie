from matplotlib import pyplot as plt
import openpyxl as px
import numpy as np
import secrets

FILE_NAME = '8_2-all_vehicle'
SHEET_NAME = 'Average'
START_POS_X = 2
START_POS_Y = 2
DATA_ITEMS = 3
DATA_INTERVAL = 24


# ファイルパスを返す
def getFilePath(seed=-1, plusname=''):
    if seed == -1:
        return secrets.DIRECTRY_PATH + secrets.DIRECTRY_NAME + '/'
    else:
        return secrets.DIRECTRY_PATH + secrets.DIRECTRY_NAME + '/seed' + str(secrets.START_NUMBER + seed) + plusname


def readExcelCells():
    # data_only=Trueにすると、cell.valueで計算式ではなく計算結果が取れる
    wb = px.load_workbook(getFilePath() + FILE_NAME + '.xlsx', data_only=True)
    ws = wb.active

    buf = [[-1 for row in range(secrets.MAX_AREA_COUNT)] for col in range(DATA_ITEMS)]
    for y in range(DATA_ITEMS):
        for x in range(secrets.MAX_AREA_COUNT):
            cell = ws.cell(row=START_POS_X + x * DATA_INTERVAL, column=START_POS_Y + y * DATA_INTERVAL)
            buf[y][x] = cell.value

    return buf


def main():
    cells = readExcelCells()
    xAxis = [360*count for count in range(1, secrets.MAX_TIME_COUNT+1)]
    plt.scatter()
    plt.xlabel('時間(s)')  # x軸
    plt.ylabel('人数(人)')  # y軸
    plt.show()  # グラフの描画


if __name__ == '__main__':
    print(getFilePath())
    main()
