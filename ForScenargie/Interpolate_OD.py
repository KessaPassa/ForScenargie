import pandas as pd
import numpy as np
import env


def get_read_path():
    return env.ROOT_DIR + 'OD/'


def get_write_path():
    return env.ROOT_DIR + 'Interpolated_OD/'


# NaNではない最初の値のindexを返す
def find_not_nan_index(_list):
    index = -1

    for key, value in enumerate(_list):
        if not np.isnan(value):
            index = key

    return index


# NaNになっている時間を補間する
def interpolate_times(df):
    # {'3600': 0,
    #  '21600': 5,
    #  'is_arrived': 6}
    new_times = []
    for row in np.asanyarray(df):
        times = np.delete(row, -1)

        # 最初の取得時間3600がNaNなら出現していないので、自宅に居た体で補間
        if np.isnan(times[0]):
            index = find_not_nan_index(times)
            for i in range(0, index):
                times[i] = times[index]

        # is_arrived == Trueなら目的地に着いて消えてるので、遊んでいる体で補間
        if row[6] == True:
            times = times[::-1]
            index = find_not_nan_index(times)
            for i in range(0, index):
                times[i] = times[index]
            times = times[::-1]

        new_times.append(times)

    return pd.DataFrame(new_times)


if __name__ == '__main__':
    dir_list = ['2_8', '4_6', '6_4', '8_2']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT)]
    times_list = [str(3600 * (i + 1)) for i in range(6)]

    csv_array = {}
    for _dir in dir_list:
        csv_array[_dir] = {}
        for _seed in seed_list:
            csv_array[_dir][_seed] = pd.read_csv(get_read_path() + _dir + 'seed' + _seed + '.csv', index_col=0)
            csv_array[_dir][_seed] = csv_array[_dir][_seed].loc[csv_array[_dir][_seed]['type'] == ' Vehicle']

            # indexを再度割り振りしてやらないと最後の方が空白になってしまう
            csv_array[_dir][_seed].reset_index(drop=True, inplace=True)

            csv_array[_dir][_seed][times_list] = interpolate_times(csv_array[_dir][_seed][times_list + ['is_arrived']])
            # csv_array[_dir][_seed].dropna(how='any', inplace=True)
            csv_array[_dir][_seed].to_csv(get_write_path() + _dir + 'seed' + _seed + '.csv')
            print(_dir + 'seed' + _seed + '.csv')
