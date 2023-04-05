#import
import random
from pathlib import Path
import cv2
import pandas as pd
from . import param as prm

prj_path = Path(__file__).resolve().parent

#関数宣言
#ボルトリストの作成 [[num,x,y],[num,x,y],...]
def make_list(filename):
    list_csv = pd.read_csv(filename,header=None).values.tolist()
    
    list_f = []
    for i in range(prm.MAX_NUM):
        list_temp = [i]
        list_temp.append(list_csv[i][0])
        list_temp.append(list_csv[i][1])
        list_f.append(list_temp)
    return list_f


#スタート足候補
def start_foot_list(input_height,input_list):
    list_start_foot_f = []
    for i in range(prm.MAX_NUM):
        if input_list[i][2] >= input_height:
            list_start_foot_f.append(i)
    return list_start_foot_f


#ルートセット
def route_set(input_sf,input_list):
    list_route_f = [input_list[input_sf]]

    list_p = []
    p = 0
    k = 0
    j = 0
    while j <= prm.MAX_NUM:
        j = j+1
        for i in range(prm.MAX_NUM):
            h = input_list[i][2]-list_route_f[k][2]
            if h <= 0:
                h = h*(-1)
                r = ((input_list[i][1]-list_route_f[k][1])**2 + h**2)**0.5
                if r <= prm.REACH:
                    ph = prm.REACH*0.6*2 - abs(h-prm.REACH*0.6)
                    pr = prm.REACH*0.6*2 - abs(r-prm.REACH*0.6)
                    p = p + ph*pr
                    list_temp = [i,p]
                    list_p.append(list_temp)
        rd = random.random()
        for l in range(len(list_p)):
            q = (list_p[l][1])/p
            if rd < q:      
                list_route_f.append(input_list[list_p[l][0]])
                k = k+1
                p = 0
                list_p = []
                break
        if list_route_f[k][2] <= prm.GOAL_HEIGHT:
            break
    return list_route_f

# 関数
def make():
    list = make_list(prj_path.joinpath('csv/hold_list.csv'))

    list_start_foot = start_foot_list(prm.START_FOOT_HEIGHT,list)

    sf = random.choice(list_start_foot)

    list_route = route_set(sf,list)
    
    return list_route    


# 描画
def print_prj(list_route):
    img = cv2.imread(str(prj_path.joinpath('image/aveu.png')))

    h, w, _ = img.shape
    resize_rate = 900/h
    wall = cv2.resize(img, (int(w*resize_rate), 900))

    start_flag = 0
    for i in range(len(list_route)-1):
        x = list_route[i][1]
        y = list_route[i][2]
        if start_flag ==0:
            if y < prm.START_HEIGHT:
                cv2.circle(wall, center=(x, y), radius=30, color=(0, 0, 255), thickness=3, lineType=cv2.LINE_4, shift=0)
                start_flag = 1         
            else:
                cv2.circle(wall, center=(x, y), radius=20, color=(0, 255, 0), thickness=3, lineType=cv2.LINE_4, shift=0)
        else:
            cv2.circle(wall, center=(x, y), radius=20, color=(0, 255, 0), thickness=3, lineType=cv2.LINE_4, shift=0)

    
    x = list_route[len(list_route)-1][1]
    y = list_route[len(list_route)-1][2]
    cv2.circle(wall, center=(x, y), radius=30, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_4, shift=0)
        
    # cv2.imshow('output', wall)
    # cv2.waitKey(0)
    cv2.imwrite(str(prj_path.parent.parent.joinpath('media_local/output.png')), wall)
    cv2.imwrite(str(prj_path.joinpath('image/output.png')), wall)
    