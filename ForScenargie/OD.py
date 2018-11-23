import numpy as np
import pandas as pd
import env


def get_read_path():
    return env.ROOT_DIR + 'Origin/'


def get_write_path():
    return env.ROOT_DIR + 'OD/'


def create_base_dataframe():
    times_list = [3600 * (i + 1) for i in range(6)]
    columns = ['id', 'type']
    columns.extend(times_list)

    df = pd.DataFrame(columns=columns)
    return df


def distribute_od(base, read):
    """
    :type base: pd.DataFrame
    :type read: pd.DataFrame
    """

    tmp_dic = {}
    # rの配列番号対応 {id: 0, type: 1, time: 2, area: 3}
    for value in np.asanyarray(read):
        tmp_dic[str(value[0])] = value

    for key, value in tmp_dic.items():
        row = base.loc[base['id'] == value[0]]

        # もし空なら新しく行を作成し、追加
        # row.empty
        if len(row.index) == 0:
            columns_list = [value[0], value[1]]
            index, times_list = split_type(value[2])
            times_list[index] = value[3]
            columns_list.extend(times_list)

            tmp = pd.Series(columns_list, index=base.columns)
            base = base.append(tmp, ignore_index=True)

        # 既に同じIDがあるなら時間帯のエリアを追加
        else:
            # print('エルス')
            base.loc[row.index, ['type', value[2]]] = [value[1], value[3]]
            print(base.loc[row.index, ['type', value[2]]])
            # row['type'] = value[1]
            # row[str(value[2])] = value[3]

    return base


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


if __name__ == '__main__':
    df_base = create_base_dataframe()
    # hoge = pd.Series([62378, 'Vehicles', 21, 22, 23, 24, np.nan, 26], index=df_base.columns)
    # df_base = df_base.append(hoge, ignore_index=True)

    dir_list = ['2_8', '4_6', '6_4', '8_2']
    seed_list = [str(123 + i) for i in range(10)]

    for _dir in dir_list:
        for _seed in seed_list:
            # print(_dir + '_seed' + _seed)
            df_read = pd.read_csv(get_read_path() + _dir + '_seed' + _seed + '.csv',
                                  encoding='Shift_JISx0213')
            df_read = df_read.loc[:, ['id', 'type', 'time', 'area']]
            result = distribute_od(df_base.copy(), df_read)
            result.to_csv(get_write_path() + _dir + 'seed' + _seed + '.csv')
            print(_dir + 'seed' + _seed + '.csv')
