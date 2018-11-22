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
        row = base.loc[base['id'] == value[0], 'id']
        if row is not None:
            print(row)
            row['type'] = value[1]
            row[value[2]] = value[3]
        else:
            columns_list = [value[0], value[1]]
            columns_list.append(split_type(value[2]))
            print(columns_list)

            tmp = pd.Series(columns_list, index=base.columns)
            base = base.append(tmp, ignore_index=True)
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
    return times_list


if __name__ == '__main__':
    df_base = create_base_dataframe()
    # hoge = pd.Series([0, 1, 2, 3, 4, 5, 6, 7], index=df_base.columns)
    # df_base = df_base.append(hoge, ignore_index=True)

    dir_list = ['2_8', '4_6', '6_4', '8_2']
    seed_list = [str(123 + i) for i in range(10)]

    for _dir in dir_list:
        for _seed in seed_list:
            # print(_dir + '_seed' + _seed)
            df_read = pd.read_csv(get_read_path() + _dir + '_seed' + _seed + '.csv',
                                  encoding='Shift_JISx0213',
                                  dtype=None,
                                  delimiter=',')
            df_read = df_read.loc[:, ['id', 'type', 'time', 'area']]
            result = distribute_od(df_base.copy(), df_read)
