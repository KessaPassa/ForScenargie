import env
import sys
import pandas as pd
import numpy as np

read_dir_name = 'od_from_bigdata'
write_dir_name = 'next_move_area'


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


def main(args):
    df = pd.read_csv(env.get_full_path(read_dir_name, args),
                     names=env.get_col_names(),
                     encoding='Shift_JISx0213')

    for _area in env.get_area_list():
        df_area = create_next_move_area(df, _area)
        df_area.to_csv(
            env.get_full_path(write_dir_name, args, any=_area),
            index=False)


if __name__ == '__main__':
    if not env.check_write_dir(write_dir_name):
        print('プログラムを終了します')
        sys.exit()

    env.for_default(main)
