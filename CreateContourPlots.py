import openpyxl as px
import numpy as np
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


def createContourPlots(Z):
    x = np.arange(0, secrets.MAX_AREA_COUNT, 1)  # x軸の描画範囲の生成。0から10まで0.05刻み。
    y = np.arange(360, 2160 + 360, 360)  # y軸の描画範囲の生成。0から10まで0.05刻み。
    X, Y = np.meshgrid(x, y)

    # cmapは_rをつけると色の向きが逆になる
    plt.pcolormesh(X, Y, Z, cmap='RdYlGn_r')  # 等高線図の生成。cmapで色付けの規則を指定する。
    pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
    #pp.set_label("Number", fontname="Arial", fontsize=18)  # カラーバーのラベル
    #plt.grid(which='major')

    #plt.xlabel('Area', fontsize=18)
    #plt.ylabel('Time(s)', fontsize=18)

    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    plt.yticks([360, 720, 1080, 1440, 1800, 2160])

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
    # tmp = np.array(Z)
    # Z = tmp.transpose()

    createContourPlots(Z)
