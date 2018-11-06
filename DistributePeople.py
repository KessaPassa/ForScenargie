import pandas as pd
import numpy as np

root_dir = '/Users/kessapassa/OneDrive/research_log/logs/'
output_dir = root_dir + 'output/'


# エリアと時間別に人数を+1ずつしていく
def distributePeople(value):
    poeple_by_area_time = np.zeros((36, 6))
    poeple_by_area_time = pd.DataFrame(poeple_by_area_time, columns=[3600 * (i + 1) for i in range(6)])
    for r in np.asanyarray(value):
        poeple_by_area_time.loc[r[6], int(r[2])] += 1
    # poeple_by_area_time.to_csv(output_dir + str(key) + dir + '_' + str(seed) + '.csv')
    # print(str(key) +  dir + '_' + str(seed) + '.csv')
    df_array = poeple_by_area_time
    return df_array


def createPeopleDataframe():
    return pd.DataFrame(np.zeros((36, 6)), columns=[3600 * (i + 1) for i in range(6)])


if __name__ == '__main__':
    # 自動車と歩行者の割合
    dir_list = ['2_8', '4_6', '6_4', '8_2']

    for dir in dir_list:
        # seedを全てプラスして格納する箱を初期化しとく
        df_array = {'mobile': createPeopleDataframe(), 'census': createPeopleDataframe(), 'vehicles': createPeopleDataframe(), 'pedestrians': createPeopleDataframe()}

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
                df_array[key] += distributePeople(value)

        print(dir)
        for key, value in df_array.items():
            df_array[key] /= 10
            df_array[key].to_csv(output_dir + str(key) + dir + '.csv')
