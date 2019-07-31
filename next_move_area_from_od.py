import env
import sys
import pandas as pd
import numpy as np

read_dir_name = 'Origin'
write_dir_name = 'next_move_area'

is_remove_oririn = False

road_to_area = {}


def func_road_to_area(args):
    df = pd.read_csv(env.get_full_path('include_area_-1', args),
                     encoding='Shift_JISx0213')
    df = df.loc[:, ['road', 'area']]
    for row in np.asanyarray(df):
        road_to_area[row[0]] = float(row[1])
        # create_road_to_area(row[0], row[1])

    road_to_area[np.nan] = np.nan


def extract_only_area(series):
    row = series.values.tolist()
    # print(row[2:])
    df_new = row[0:3]
    df_base = []
    stack = -1

    for i in range(len(row)):
        if (i >= 3) and (type(row[i]) is str) and ('(census)' in row[i]):
            road_name = row[i].split('(census)')[0]
            _area = road_to_area[road_name]

            if is_remove_oririn:
                # 移動した場合のみ記録するので、同じエリアに居る場合は削除
                if stack != _area:
                    df_base.append(_area)
                stack = _area
            else:
                df_base.append(_area)

    df_new.extend(df_base)

    return pd.Series(df_new)


def create_next_move_area(df, area):
    area = float(area)
    df_area = pd.DataFrame(np.zeros((81, 2)), columns=['area', 'people'])
    df_area['area'] = [float(i) for i in range(81)]

    for row in df.values.tolist():
        if area in row:
            index = row.index(area)
            if (len(row) > index + 1) and (not np.isnan(row[index + 1])):
                df_area.loc[df_area['area'] == row[index + 1], 'people'] += 1

    return df_area


# dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes]
#
#
# def remove_and_fill_none_area(series):
#     row = series.values.tolist()
#     if -1 in row:
#         # -1のindexをリストで取得
#         index_list = [i for i, x in enumerate(row) if x == -1]
#         # popと同じような原理で削除し横詰め
#         row = dellist(row, index_list)
#         # 削除した分、ズレが生じるので最後尾に消した数のNaNを追加
#         row.extend([np.nan for i in range(len(index_list))])
#
#         return pd.Series(row, index=series.index)
#     else:
#         return series


def main(args):
    # road_to_area = {}
    # func_road_to_area(args, road_to_area)

    df = pd.read_csv(env.get_full_path(read_dir_name, args),
                     names=env.get_col_names(),
                     encoding='Shift_JISx0213')
    #     df = df.dropna(how='all')
    df = df.apply(lambda x: extract_only_area(x), axis=1)

    # df.iloc[:, 3:] = df.iloc[:, 3:].applymap(lambda x: road_to_area[x])
    # df = df[df.loc[:, 'c03'] >= 0]
    # dfT = df.T
    # dfT = dfT.apply(remove_and_fill_none_area)
    # df = dfT.T
    # df.reset_index(drop=True, inplace=True)
    # #             df = pd.concat([df_id, df], axis=1)
    # df = df.rename(columns={'c00': 'id'})
    # df = df.sort_values(['id'])
    # df = df.drop(['c01', 'c02'], axis=1)
    #
    # df.replace(' ', np.NaN, inplace=True)
    # df.dropna(how='all', axis=1, inplace=True)

    df = df.applymap(lambda x: (x.split('(census)')[0]) if (type(x) is str) and ('(census)' in x) else x)

    for _area in env.get_area_list():
        df_area = create_next_move_area(df.copy(), _area)
        df_area.to_csv(env.get_full_path(write_dir_name, args, any=_area), index=False)


if __name__ == '__main__':
    if not env.check_write_dir(write_dir_name):
        print('プログラムを終了します')
        sys.exit()

    env.for_default(func_road_to_area, csv=['census'])
    env.for_default(main, csv=['od'])
