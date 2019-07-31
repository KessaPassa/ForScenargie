import pandas as pd
import numpy as np
import env
import time

road_to_area = {}
df_base = {}


def create_road_to_area(road, area):
    road_to_area[road] = float(area)


def func_road_to_area(args):
    df = pd.read_csv(env.get_full_path('include_area_-1', args),
                     encoding='Shift_JISx0213')
    df = df.loc[:, ['road', 'area']]
    for row in np.asanyarray(df):
        create_road_to_area(row[0], row[1])

    road_to_area[np.nan] = np.nan


def interpolate_time(time):
    time = int(time)
    times_list = [3600 * (i + 1) for i in range(6)]
    times = ''

    if 0 <= time <= times_list[0]:
        times = times_list[0]
    elif times_list[0] <= time <= times_list[1]:
        times = times_list[1]
    elif times_list[1] <= time <= times_list[2]:
        times = times_list[2]
    elif times_list[2] <= time <= times_list[3]:
        times = times_list[3]
    elif times_list[3] <= time <= times_list[4]:
        times = times_list[4]
    elif times_list[4] <= time <= times_list[5]:
        times = times_list[5]

    return times


def create2d(args, array):
    df = np.zeros((6 * 81, 3))
    df = pd.DataFrame(df, columns=['time', 'area', 'people'])

    index = 0
    for _time in range(6):
        for area in range(81):
            df.loc[index, ['time', 'area']] = [[3600 * (_time + 1), area]]
            index += 1
    array[args.dir][args.ratio][args.seed][args.csv] = df.copy()


def distribute(df, args):
    for row in df.values.tolist():
        tmp = row[0:2]
        stack = -1
        for i in range(len(row)):
            if (i >= 3) and (type(row[i]) is str) and ('(census)' in row[i]):
                road_name = row[i].split('(census)')[0]
                _area = road_to_area[road_name]

                # if stack != _area:
                _time = interpolate_time(row[i].split('@')[1])
                df = df_base[args.dir][args.ratio][args.seed][args.csv]
                # stack = _area

                df.loc[(df['time'] == _time) & (df['area'] == _area), 'people'] += 1


def main(args):
    start = time.time()
    col_names = ['c{0:02d}'.format(i) for i in range(30)]
    df = pd.read_csv(env.get_full_path('Origin', args),
                     names=col_names,
                     encoding='Shift_JISx0213')

    df.replace(' ', np.NaN, inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    distribute(df.copy(), args)

    df_base[args.dir][args.ratio][args.seed][args.csv].to_csv(env.get_full_path('2D', args), index=False)

    print(env.get_file_name(args))
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")


if __name__ == '__main__':
    env.for_default(func_road_to_area, ['census'])
    env.for_default_init(create2d, df_base)
    env.for_default(main, ['od'])
