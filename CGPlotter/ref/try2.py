'''=============================='''
'''     Date: 2022/03/12         '''
''' TDPL data processing attempt '''
'''      Author: Ceress Goo      '''
'''=============================='''

#%% import

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as spsg



#%% function

'''================================[function]============================'''

def get_data_raw(datadir, temp):                #read raw csv data
    df = pd.read_csv(datadir+str(temp)+'.csv', header=None, names=['wl', 'inten'])
    return df

def get_data_normed(datadir, temp):             #read csv data and normalize it
    df = pd.read_csv(datadir+str(temp)+'.csv', header=None, names=['wl', 'inten'])
    max_inten = df.inten.values.max()
    df.inten = df.inten / max_inten
    return df

def data_sel_range(df, center_wl, rang_width):           #return data in selected wavelength range as pd.dataframe
    wlmax = center_wl + (rang_width / 2)
    wlmin = center_wl - (rang_width / 2)
    return df[(df['wl'] < wlmax) & (df['wl'] > wlmin)]

def data_upshift(df, idx):                      #shift curve upwards by 0.1*curveindex
    newdf = df
    newdf.inten = df.inten + 0.1 * idx
    return newdf

def plot_add_line(df, idx):                     #add a line during plting
    df.inten = df.inten + 0.1 * idx
    plt.plot(df.wl.values, df.inten.values)

def find_peak_smooth(df_raw):
    inten_smth = spsg.savgol_filter(df_raw.inten.values, 31, 2)
    df_raw.inten = inten_smth
    max_inten = inten_smth.max()
    df_max = df_raw[df_raw['inten']==max_inten]
    return df_max.wl.values[0]

def generate_peak_T(sample_name):
    datadir = f'../data/{sample_name}/'
    temp_list = list(range(-195, 105, 15))

    df_peak_T = pd.DataFrame(columns=('kelvin', 'wl'))

    for temp in temp_list:
        if os.path.exists(datadir+f'{temp}.csv'):
            df_raw = get_data_raw(datadir, temp)
            max_wl = find_peak_smooth(df_raw)
            df_datapoint = pd.DataFrame({'kelvin':[temp+273], 'wl':[max_wl]})
            df_peak_T = df_peak_T.append(df_datapoint, ignore_index=True)
    # by now, the kelvin - maximum wavelength pair is stored in df_peak_T.
    return df_peak_T

def savetxt_peak_T(df_peak_T, sample_name):
    temp = df_peak_T.kelvin.values
    wl = df_peak_T.wl.values
    dflen = len(temp)
    with open(f'../report/TDPL/{sample_name}.txt', 'w', encoding='utf-8') as rep:
        for i in range(dflen):
            rep.write(f'{temp[i]} {wl[i]}\n')



#%% main

'''========================[work]================================'''

sample_name = 'PEA'
datadir = f'../data/{sample_name}/'
graphdir = '../graph/test1/'
temp_list = list(range(-195, 105, 15))

#setting plt params

fig = plt.figure(figsize=(6,5), dpi=300)
cmap = plt.get_cmap('plasma')
colors = [cmap(i) for i in np.linspace(0,1,22)]
# ax1 = plt.subplot(1,2,1)


plt.title(f'TDPL Spectrum of {sample_name}')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (a.u.)')
plt.yticks([])


#plotting TDPL curves

idx = 0
for temp in temp_list:
    if os.path.exists(datadir+f'{temp}.csv'):
        df_raw = get_data_normed(datadir, temp)
        df_focus = data_sel_range(df_raw, 505, 60)
        df = data_upshift(df_focus, idx)
        plt.plot(df.wl.values, df.inten.values, label=f'{temp+273} K', color=colors[idx], linewidth=1.5)
        idx += 1

plt.legend(loc='upper right', labelspacing=0.05, fontsize=8)
plt.savefig(graphdir+f'{sample_name}.png')
plt.show()


#all-range TDPL specs

#setting plt params

fig = plt.figure(figsize=(6,5), dpi=300)
cmap = plt.get_cmap('plasma')
colors = [cmap(i) for i in np.linspace(0,1,22)]
# ax1 = plt.subplot(1,2,1)


plt.title(f'TDPL Spectrum of {sample_name} - full')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (a.u.)')
plt.yticks([])


#plotting TDPL curves

idx = 0
for temp in temp_list:
    if os.path.exists(datadir+f'{temp}.csv'):
        df_raw = get_data_normed(datadir, temp)
        df = data_upshift(df_raw, idx)
        plt.plot(df.wl.values, df.inten.values, label=f'{temp+273} K', color=colors[idx], linewidth=0.8)
        idx += 1

plt.legend(loc='upper right', labelspacing=0.05, fontsize=8)
plt.savefig(graphdir+f'{sample_name}-full.png')
plt.show()


#%% plot the peak_wavelength - Temp graph

# sample name libraries.
# if u want to compare selected series of samples, change the lib in the for loop below.
sample_lib_all = ['PMA', 'PEA', 'R-MBA', 'S-MBA', 'rac-MBA', 'AMP', '4FBzA', '4ClBzA', '4BrBzA']

sample_lib_4x = ['PMA', '4FBzA', '4ClBzA', '4BrBzA']
sample_lib_pma = ['PMA', 'PEA']
sample_lib_mba = ['R-MBA', 'S-MBA', 'rac-MBA']
sample_lib_amp = ['AMP']

# setting plt parameters

fig = plt.figure(figsize=(5,5), dpi=300)

plt.title(f'PL peaks under different T')
plt.xlabel('Temperature (K)')
plt.ylabel('PL peak (nm)')

for sample_name in sample_lib_all:               # edit here to change selected samples
    df_peak_T = generate_peak_T(sample_name)
    plt.plot(df_peak_T.kelvin.values, df_peak_T.wl.values, marker='o', markersize=3, label=sample_name)

    savetxt_peak_T(df_peak_T, sample_name)      # quote this line if u dont need to save the kelvin-wl result as .txt

# plt.legend(bbox_to_anchor=(1.4, 0.7))
plt.legend()
plt.savefig('../graph/TDPL/peak_T_relation/all.png')    # remember to change the file name here!!
plt.show()









#%% savgol plgnd 1


'''==========================[playground]=========================='''

df_raw = get_data_raw(datadir, 75)

inten_raw = df_raw['inten'].values
inten_smth = spsg.savgol_filter(inten_raw, 21, 3)

print(f'raw length = {len(inten_raw)}\nsmooth length = {len(inten_smth)}')

fig = plt.figure(figsize=(10,5), dpi=500)

plt.plot(df_raw.wl.values, inten_raw, color='r')
plt.plot(df_raw.wl.values, inten_smth, color='b')
plt.xlim(515,550)
plt.ylim(4000, 5000)
plt.savefig('../graph/test1/smooth test1.png')
plt.show()

#%% savgol plgnd 2

peak_wl = find_peak_smooth(df_raw)
print(peak_wl, type(peak_wl))


#%% plgnd 4

datadir = '../data/PMA/'
temp_list = list(range(-195, 105, 15))

df = get_data_normed(datadir, -120)
df_sel = data_sel_range(df, 600, 500)
print(df_sel)





#%% plgnd 3
sample_name = 'PEA'
datadir = f'../data/{sample_name}/'
grphdir = '../graph/test1/'
temp_list = list(range(-195, 105, 15))



fig1 = plt.figure(figsize=(5,5), dpi=300)
plt.title(f'TDPL Spectrum of {sample_name}')
plt.xlabel('Wavelength (nm)')
plt.yticks([])
plt.ylabel('Intensities (a.u.)')
cmap = plt.get_cmap('plasma')
colors = [cmap(i) for i in np.linspace(0,1,21)]

idx = 0
for temp in temp_list:
    if os.path.exists(datadir+f'{temp}.csv'):
        df_raw = get_data_normed(datadir, temp)
        df = data_sel_range(df_raw, 525, 60)
        df.inten = df.inten + 0.1 * idx
        plt.plot(df.wl.values, df.inten.values, color=colors[idx])
        idx += 1
plt.savefig(grphdir+f'{sample_name}.png')
plt.show()


#%% plgnd 2
datadir = '../data/PMA/'
temp = -120
df = pd.read_csv(datadir+str(temp)+'.csv', header=None, names=['wl', 'inten'])

max_inten = df['inten'].values.max()
df.inten = df.inten / max_inten             #Normalization by dividing the maximum intensity

fig1 = plt.figure(figsize=(5,5), dpi=300)
plt.plot(df.wl.values, df.inten.values)
plt.show()







#%% plgnd

datadir = '../data/0122AMP/raw/'
temp_list = list(range(-195, 105, 15))

for temp in temp_list:
    if os.path.exists(datadir + str(temp) + '.csv'):
        print(f'data exists for T={temp}')
    else:
        print(f"data doesn't exist for T={temp}")


















