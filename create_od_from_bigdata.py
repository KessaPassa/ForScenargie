import env
import sys
import pandas as pd
import numpy as np

read_dir_name = 'Origin'
write_dir_name = 'od_from_bigdata'


def main(args, array):
    df = pd.read_csv(env.get_full_path(read_dir_name, args),
                     encoding='Shift_JISx0213')
    df = df.loc[:, ['id', 'time', 'area']]

    group_list = df.groupby(['id'], sort=True)
    for _id, _group in group_list:
        _group = _group.sort_values(['time'])
        # array[args.dir][args.ratio][args.seed][args.csv][_id] = []
        array[args.dir][args.ratio][args.seed][args.csv][_id] = []
        for area in np.asanyarray(_group.loc[:, 'area']):
            array[args.dir][args.ratio][args.seed][args.csv][_id].append(area)

    df = pd.DataFrame()
    df_main = array[args.dir][args.ratio][args.seed][args.csv].copy()
    for _id in df_main:
        df_main[_id].insert(0, _id)
        tmp = pd.DataFrame(df_main[_id]).T
        df = pd.concat([df, tmp])
    df.to_csv(env.get_full_path(write_dir_name, args), index=False)


if __name__ == '__main__':
    if not env.check_write_dir(write_dir_name):
        print('プログラムを終了します')
        sys.exit()

    csv_array = {}
    env.for_default_init(main, csv_array)
