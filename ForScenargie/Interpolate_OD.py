import pandas as pd
import numpy as np
import env

root_dir = 'C:/Users/admin/OneDrive/research_log/2018_Graduate/'


def find_not_nan_index(_list):
    index = -1

    for key, value in enumerate(_list):
        if not np.isnan(value):
            index = key

    return index


def interpolate_times(df):
    convert_dic = {
        '3600': 0,
        '21600': 5,
        'is_arrived': 6
    }

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


if __name__ == '__main__':
    dir_list = ['2_8', '4_6', '6_4', '8_2']
    seed_list = [str(123 + i) for i in range(env.MAX_SEED_COUNT)]
    times_list = [str(3600 * (i + 1)) for i in range(6)]

    csv_array = {}
    for _dir in dir_list:
        csv_array[_dir] = {}
        for _seed in seed_list:
            csv_array[_dir][_seed] = pd.read_csv(root_dir + 'OD/' + _dir + 'seed' + _seed + '.csv', index_col=0)
            csv_array[_dir][_seed] = csv_array[_dir][_seed].loc[csv_array[_dir][_seed]['type'] == ' Vehicle']
            csv_array[_dir][_seed][times_list] = interpolate_times(csv_array[_dir][_seed][times_list + ['is_arrived']])
            # csv_array[_dir][_seed].dropna(how='any', inplace=True)
            csv_array[_dir][_seed].to_csv(root_dir + 'OD2/' + _dir + 'seed' + _seed + '.csv')
            print(_dir + 'seed' + _seed + '.csv')
