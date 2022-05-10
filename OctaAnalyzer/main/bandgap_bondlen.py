# -*- coding: utf-8 -*-

'''
****************************************
bond length - bandgap analysis tool
by CeressGoo
2022.04.18
****************************************
'''

#%% import

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utilsfunction as uf
# from sklearn import linear_model, metrics
# from sklearn.preprocessing import PolynomialFeatures

#%% function









#%% main 1: bondlength - bandgap
sample_lib = ['PMA', '4FPMA', '4ClPMA', '4BrPMA', 'PEA', '4FPEA', '4ClPEA', '4BrPEA', 'R-MBA', 'S-MBA', 'rac-MBA', 'BA']
# sample_lib = ['PMA', '4FPMA']
workdir = '../data/bondlen/'

df_all = pd.DataFrame(columns=['bl', 'bg', 'name'])
df_bg = pd.read_csv('../data/bandgap/bandgap_source.csv')
for sample_name in sample_lib:
    datadir = f'{workdir}{sample_name}.txt'
    block_list = uf.read_data(datadir)
    bl_avg = uf.calc_avg_bondlen(block_list)
    bg = df_bg.query(f'name == ["{sample_name}"]')['bg'].values[0]
    df_all = df_all.append({'bl':bl_avg, 'bg':bg, 'name':sample_name}, ignore_index=True)
print(df_all)

df_all.to_csv('../report/bg-bl_relationship.csv', index=None)


fig = plt.figure(figsize=(5,5), dpi=300)

x = df_all.bl.values
y = df_all.bg.values
names = df_all.name.values
plt.scatter(x, y, marker='x', color='red')
for idx in range(len(names)):
    plt.annotate(names[idx], xy=(x[idx], y[idx]), xytext=(x[idx]+0.001, y[idx]+0.001), fontsize=7)

plt.title('Bondlength - bandgap relationship')
plt.xlabel('Bondlength (A)')
plt.ylabel('Bandgap (eV)')
plt.savefig('../graph/bg-bl_relation.png')
plt.show()




#%% main 2: bondlength std - bandgap

sample_lib = ['PMA', '4FPMA', '4ClPMA', '4BrPMA', 'PEA', '4FPEA', '4ClPEA', '4BrPEA', 'R-MBA', 'S-MBA', 'rac-MBA', 'BA']
# sample_lib = ['PMA', '4FPMA']
workdir = '../data/bondlen/'

df_all = pd.DataFrame(columns=['std', 'bg', 'name'])
df_bg = pd.read_csv('../data/bandgap/bandgap_source.csv')
for sample_name in sample_lib:
    datadir = f'{workdir}{sample_name}.txt'
    block_list = uf.read_data(datadir)
    std_avg = uf.calc_avg_std(block_list)
    bg = df_bg.query(f'name == ["{sample_name}"]')['bg'].values[0]
    df_all = df_all.append({'std':std_avg, 'bg':bg, 'name':sample_name}, ignore_index=True)
print(df_all)

df_all.to_csv('../report/bg-std_relationship.csv', index=None)


fig = plt.figure(figsize=(5,5), dpi=300)

x = df_all['std'].values
y = df_all.bg.values
names = df_all.name.values
plt.scatter(x, y, marker='x', color='red')
for idx in range(len(names)):
    plt.annotate(names[idx], xy=(x[idx], y[idx]), xytext=(x[idx]+0.001, y[idx]+0.001), fontsize=7)

plt.title('Bondlength - bandgap relationship')
plt.xlabel('Bondlength std variance (A)')
plt.ylabel('Bandgap (eV)')
plt.savefig('../graph/bg-std_relation.png')
plt.show()


#%% test 1

df = pd.DataFrame({'name':['a', 'b', 'c'], 'value':[1,2,3]})
res = df.query('name == ["a"]')
print(res, type(res))
val = res.value.values[0]
print(val, type(val))






































