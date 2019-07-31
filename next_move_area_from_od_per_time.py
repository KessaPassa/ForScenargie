import env
import sys
import pandas as pd
import numpy as np

read_dir_name = 'Origin'
write_dir_name = 'next_move_area'

road_to_area = {}


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


def extract_only_area(series):
    row = series.values.tolist()
    df_new = row[0:3]
    df_base = []

    for i in range(len(row)):
        if (i >= 3) and (type(row[i]) is str) and ('(census)' in row[i]):
            road_name = row[i].split('(census)')[0]
            _area = road_to_area[road_name]
            df_base.append(_area)

    df_new.extend(df_base)

    return pd.Series(df_new)


def main(args):
    df = pd.read_csv(env.get_full_path(read_dir_name, args),
                     names=env.get_col_names(),
                     encoding='Shift_JISx0213')
    df = df.apply(lambda x: extract_only_area(x), axis=1)
    df = df.applymap(lambda x: (x.split('(census)')[0]) if (type(x) is str) and ('(census)' in x) else x)

    for _area in env.get_area_list():
        df_area = create_next_move_area(df.copy(), _area)
        df_area.to_csv(env.get_full_path(write_dir_name, args, any=_area), index=False)


def func_road_to_area(args):
    df = pd.read_csv(env.get_full_path('include_area_-1', args),
                     encoding='Shift_JISx0213')
    df = df.loc[:, ['road', 'area']]
    for row in np.asanyarray(df):
        road_to_area[row[0]] = float(row[1])

    road_to_area[np.nan] = np.nan


if __name__ == '__main__':
    if not env.check_write_dir(write_dir_name):
        print('プログラムを終了します')
        sys.exit()

    env.for_default(func_road_to_area, csv=['census'])
    env.for_default(main, csv=['od'])
