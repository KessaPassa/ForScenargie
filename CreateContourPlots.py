import openpyxl as px
import numpy as np
import matplotlib.pyplot as plt
import secrets
import seaborn as sns

FILE_NAME = ''
SHEET_NAME = 'Average'

# START_POS_X = 2
# START_POS_Y = 56
# RANGE_X = secrets.MAX_TIME_COUNT
# RANGE_Y = secrets.MAX_AREA_COUNT


START_POS_X = 7
START_POS_Y = 2
RANGE_X = 3
RANGE_Y = 4
DETAIL_X = [0, RANGE_X+1, 1]
DETAIL_Y = [0, RANGE_Y+1, 1]

X_LABEL = 'エリア番号'
Y_LABEL = '時間(s)'
Z_LABEL = '人数'


# ファイルパスを返す
def getFilePath(seed=-1, plusname=''):
    if seed == -1:
        return secrets.DIRECTRY_PATH + secrets.DIRECTRY_NAME
    else:
        return secrets.DIRECTRY_PATH + secrets.DIRECTRY_NAME + '/seed' + str(secrets.START_NUMBER + seed) + plusname


def createContourPlots(Z):
    # x = np.arange(360, 2160 + 360, 360)  # y軸の描画範囲の生成。0から10まで0.05刻み。
    # y = np.arange(0, RANGE+X+1, 1)  # x軸の描画範囲の生成。0から10まで0.05刻み。
    # x = np.arange(DETAIL_X[0], DETAIL_X[1], DETAIL_X[2])
    # y = np.arange(DETAIL_Y[0], DETAIL_Y[1], DETAIL_Y[2])
    # X, Y = np.meshgrid(x, y)
    sns.heatmap(Z, annot=True, fmt='1.2f', cmap='RdYlGn_r')

    # cmapは_rをつけると色の向きが逆になる
    # plt.pcolormesh(X, Y, Z, cmap='RdYlGn_r')  # 等高線図の生成。cmapで色付けの規則を指定する。
    # pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
    # pp.set_label('', fontname="Arial", fontsize=18)  # カラーバーのラベル
    # plt.grid(which='major')

    # plt.xlabel(X_LABEL, fontsize=18)
    # plt.ylabel(Y_LABEL, fontsize=18)

    # plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
    # plt.xticks([360, 720, 1080, 1440, 1800, 2160])

    plt.show()


def readExcelCells():
    # data_only=Trueにすると、cell.valueで計算式ではなく計算結果が取れる
    wb = px.load_workbook(getFilePath() + FILE_NAME + '.xlsx', data_only=True)
    ws = wb.active

    buf = [[-1 for row in range(RANGE_Y)] for col in range(RANGE_X)]
    for x in range(RANGE_X):
        for y in range(RANGE_Y):
            cell = ws.cell(row=START_POS_Y + y, column=START_POS_X + x)
            buf[x][y] = cell.value

    return buf


if __name__ == '__main__':
    Z = readExcelCells()

    # 行と列を反転
    tmp = np.array(Z)
    Z = tmp.transpose()

    createContourPlots(Z)
