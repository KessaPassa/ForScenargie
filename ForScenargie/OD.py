import numpy as np
import pandas as pd
import threading
import env


def get_read_path():
    return env.ROOT_DIR + 'Origin/'


def get_write_path():
    return env.ROOT_DIR + 'OD/'


# 出力元となるdataframeの雛形
def create_base_dataframe():
    times_list = [3600 * (i + 1) for i in range(6)]
    columns = ['id', 'type']
    columns.extend(times_list)
    columns.extend(['is_arrived'])

    df = pd.DataFrame(columns=columns)
    return df


# idを元に時間別所在エリアを記述
def distribute_od(base, read):
    """
    :type base: pd.DataFrame
    :type read: pd.DataFrame
    """
    for value in np.asanyarray(read):
        row = base.loc[base['id'] == value[0]]

        # もし空なら新しく行を作成し、追加
        # row.empty
        if len(row.index) == 0:
            columns_list = [value[0], value[1]]
            index, times_list = split_type(value[2])
            times_list[index] = value[3]
            columns_list.extend(times_list)
            columns_list.extend([value[4]])

            tmp = pd.Series(columns_list, index=base.columns)
            base = base.append(tmp, ignore_index=True)

        # 既に同じIDがあるなら時間帯のエリアを追加
        else:
            base.loc[row.index, ['type', value[2]]] = [value[1], value[3]]

    return base


# 時間のindexとリストを返す
def split_type(time):
    times_list = [3600 * (i + 1) for i in range(6)]
    index = times_list.index(time)
    for key, value in enumerate(times_list):
        if key == index:
            pass
        else:
            times_list[key] = np.nan
    # print(times_list)
    return index, times_list


# NaNではない最初のindexを返す
def find_not_nan_index(_list):
    index = -1

    for key, value in enumerate(_list):
        if not np.isnan(value):
            index = key

    return index


# 最初に出現していなければ、家に居たものと見て補間。1時間ごとの時間以外を取得していれば消えたことなので、目的地について遊んでいると見て補間
def interpolate_times(df):
    # convert_dic = {
    #     '3600': 0,
    #     '21600': 5,
    #     'is_arrived': 6
    # }

    new_times = []
    for row in np.asanyarray(df):
        times = np.delete(row, -1)

        if np.isnan(times[0]):
            index = find_not_nan_index(times)
            for i in range(0, index):
                times[i] = times[index]

        if row[6] == True:
            times = times[::-1]
            index = find_not_nan_index(times)
            for i in range(0, index):
                times[i] = times[index]
            times = times[::-1]

        new_times.append(times)

    return pd.DataFrame(new_times)


def multi_thread(_dir, _seed):
    # print(_dir + '_seed' + _seed)
    df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '.csv',
                          encoding='Shift_JISx0213')
    df_read = df_read.loc[:, ['id', 'type', 'time', 'area', 'is_arrived']]
    result = distribute_od(df_base.copy(), df_read)

    times_list = [str(3600 * (i + 1)) for i in range(6)]
    result = result.loc[result['type'] == ' Vehicle']
    result[times_list] = interpolate_times(result[times_list + ['is_arrived']])
    result.dropna(how='any', inplace=True)

    result.to_csv(get_write_path() + _dir + 'seed' + _seed + '.csv')
    print(_dir + 'seed' + _seed + '.csv')


if __name__ == '__main__':
    df_base = create_base_dataframe()
    # hoge = pd.Series([62378, 'Vehicles', 21, 22, 23, 24, np.nan, 26], index=df_base.columns)
    # df_base = df_base.append(hoge, ignore_index=True)

    dir_list = ['2_8', '4_6', '6_4', '8_2']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT)]

    for _dir in dir_list:
        for _seed in seed_list:
            thread = threading.Thread(target=multi_thread(_dir, _seed))
            thread.start()
            # df_read = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '.csv',
            #                       encoding='Shift_JISx0213')
            # df_read = df_read.loc[:, ['id', 'type', 'time', 'area']]
            # result = distribute_od(df_base.copy(), df_read)
            # result.to_csv(get_write_path() + _dir + 'seed' + _seed + '.csv')
            # print(_dir + 'seed' + _seed + '.csv')
