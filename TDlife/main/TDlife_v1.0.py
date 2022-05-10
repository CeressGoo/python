# -*- coding:utf-8 -*-

'''
*************************************************
Temperature-dependent lifetime analysis tool
by CeressGoo
2022.04.17
*************************************************
'''

#%% import 

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% function

def get_csv_raw(datadir):
    df_raw = pd.read_csv(datadir)
    return df_raw[['X-Value', 'Measured']]

def get_tempkelvin_list(folderdir):
    temp_list = []
    kelvin_list = []
    for filename in os.listdir(folderdir):
        temp = int(filename.split('.')[0])
        temp_list.append(temp)
        kelvin_list.append(temp+273)
    temp_list.sort()
    kelvin_list.sort()
    return [temp_list, kelvin_list]






#%% main 1
datadir = '../data/PMA/'
temp_list = get_tempkelvin_list(datadir)[0]
kelvin_list = get_tempkelvin_list(datadir)[1]

for temp in temp_list:
    df = get_csv_raw(f'{datadir}{temp}.csv')
    print(df[:5])
    break

plt.plot(df['X-Value'].values, df['Measured'].values)
plt.show()










#%% to csv

datadir = '../data/4FBzA/'
temp_list = get_tempkelvin_list(datadir)[0]
kelvin_list = get_tempkelvin_list(datadir)[1]

for temp in temp_list:
    new_txt_source = []
    with open(f'{datadir}{temp}.txt', 'r', encoding='utf-8') as rawtxt:
        for line in rawtxt:
            line_n = line.replace(' ', '')
            line_n = line_n.replace('\t', '')
            new_txt_source.append(line_n)
    with open(f'{datadir}{temp}.csv', 'w', encoding='utf-8') as rawcsv:
        for line in new_txt_source:
            rawcsv.write(line)





















