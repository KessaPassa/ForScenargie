import pandas as pd
import numpy as np

root_dir = '/Users/kessapassa/OneDrive/research_log/logs/'
output_dir = root_dir + '2D/'


# エリアと時間別に人数を+1ずつしていく
def distribute_people(df, value):
    """
    :type df: pd.DataFrame
    :type value: pd.DataFrame
    """
    for r in np.asanyarray(value):
        # 2はtime, 6はarea
        df.loc[
            (df['time'] == r[2]) & (df['area'] == r[6]),
            'people'] += 1
    return df


def create_people_dataframe():
    times_length = 6
    area_length = 36

    people_dataframe = np.zeros((times_length * area_length, 3))
    people_dataframe = pd.DataFrame(people_dataframe, columns=['time', 'area', 'people'])

    index = 0
    for time in range(0, times_length):
        for area in range(0, area_length):
            people_dataframe.loc[index, ['time', 'area']] = [[3600 * (time + 1), area]]
            index += 1

    return people_dataframe


if __name__ == '__main__':
    df = create_people_dataframe()

    # 自動車と歩行者の割合
    dir_list = ['2_8', '4_6', '6_4', '8_2']

    for dir in dir_list:
        # seedを全てプラスして格納する箱を初期化しとく

        for seed in range(123, 132 + 1):
            main_csv = pd.read_csv(root_dir + dir + '_seed' + str(seed) + '.csv',
                                   encoding='Shift_JISx0213',
                                   dtype=None,
                                   delimiter=',')
            mobile = main_csv.copy()
            census = main_csv[main_csv['road'].str.contains('census')]
            vehicles = main_csv[main_csv['type'] == ' Vehicle']
            pedestrians = main_csv[main_csv['type'] == ' Pedestrian']

            csv_list = {'mobile': mobile, 'census': census, 'vehicles': vehicles, 'pedestrians': pedestrians}
            for key, value in csv_list.items():
                output = distribute_people(df, value)
                output.to_csv(output_dir + str(key) + '_' + dir + '_seed' + str(seed) + '.csv')
                print(str(key) + '_' + dir + '_seed' + str(seed) + '.csv')
