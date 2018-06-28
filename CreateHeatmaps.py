import openpyxl as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import secrets


FILE_NAME = ''
SHEET_NAME = 'Average'
START_INDEX = 2


# ファイルパスを返す
def getFilePath(seed=-1, plusname=''):
    if seed == -1:
        return secrets.DIRECTRY_PATH + secrets.DIRECTRY_NAME
    else:
        return secrets.DIRECTRY_PATH + secrets.DIRECTRY_NAME + '/seed' + str(secrets.START_NUMBER + seed) + plusname


def createHeatmaps(Z):
    sns.set()
    sns.heatmap(Z, annot=True, fmt='1.1f', cmap='RdYlGn_r')

    plt.grid()
    plt.show()



def readExcelCells():
    # data_only=Trueにすると、cell.valueで計算式ではなく計算結果が取れる
    wb = px.load_workbook(getFilePath() + FILE_NAME + '.xlsx', data_only=True)
    ws = wb.active

    buf = [[-1 for row in range(secrets.MAX_AREA_COUNT)] for col in range(secrets.MAX_TIME_COUNT)]
    for y in range(secrets.MAX_TIME_COUNT):
        for x in range(secrets.MAX_AREA_COUNT):
            cell = ws.cell(row=2 + x, column=START_INDEX + y)
            buf[y][x] = cell.value

    return buf


if __name__ == '__main__':
    Z = readExcelCells()

    # 行と列を反転
    tmp = np.array(Z)
    Z = tmp.transpose()

    createHeatmaps(Z)
