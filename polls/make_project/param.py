from pathlib import Path
import pandas as pd

prj_path = Path(__file__).resolve().parent

#定数
#ホールド全数
MAX_NUM = sum([1 for _ in open(prj_path.joinpath('csv/hold_list.csv'))])


#ゴール高さ下限、スタート足高さ上限、スタート高さ下限
list_csv1 = pd.read_csv(prj_path.joinpath('csv/border.csv'),header=None).values.tolist()

y_ave = []
for i in range(3):
    y1 = list_csv1[i][1]
    y2 = list_csv1[i][3]
    y_ave.append((y1+y2)/2)

max = y_ave[0]
min = y_ave[0]
for i in range(3):
    if y_ave[i] > max:
        max = y_ave[i]
    if y_ave[i] < min:
        min = y_ave[i]

mid = y_ave[0]
for i in range(3):
    if y_ave[i] != min and y_ave[i] != max:
        mid = y_ave[i]

GOAL_HEIGHT = min
START_FOOT_HEIGHT = max
START_HEIGHT = mid


#リーチ 
list_csv2 = pd.read_csv(prj_path.joinpath('csv/reach.csv'),header=None).values.tolist()
REACH = ((list_csv2[0][0]-list_csv2[0][2])**2+(list_csv2[0][1]-list_csv2[0][3])**2)**0.5


# 不要になるかも？　max_x,y
list_csv = pd.read_csv(prj_path.joinpath('csv/hold_list.csv'),header=None).values.tolist()

#ゴール高さ,幅取得
MAX_X = 0
for i in range(MAX_NUM):
    if MAX_X < list_csv[i][0]:
        MAX_X = list_csv[i][0]

MAX_Y = 0
for i in range(MAX_NUM):
    if MAX_Y < list_csv[i][1]:
        MAX_Y = list_csv[i][1]
