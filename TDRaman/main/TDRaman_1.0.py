'''
****************************************************
TDRaman plotting tool
by CeressGoo
2022.04.22
****************************************************
'''


#%% import 

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% functions

def get_csv_raw(datadir):
    df = pd.read_csv(datadir, header=None, names=['wn', 'inten'])
    return df

def norm_maxdivide(df):
    max_inten = df.inten.values.max()
    df_n = df
    df_n['inten'] = df['inten'] / max_inten
    return df_n

def focus_on_range(df, wnradius):
    df_n = df[(df['wn'] > (-wnradius)) & (df['wn'] < wnradius)]
    return df_n

def get_tempkelvin_list(folderdir):             # get all temperature/kelvin integers in a list
    temp_list = []
    kelvin_list = []
    for filename in os.listdir(folderdir):
        temp = int(filename.split('.')[0])
        temp_list.append(temp)
        kelvin_list.append(temp+273)
    temp_list.sort()
    kelvin_list.sort()
    return [temp_list, kelvin_list]





#%% main 1: vstack plot

datadir = '../data/0422/'
sample_lib = ['C5', 'PMA', 'R-MBA']
cmap = plt.get_cmap('jet')

for sample_name in sample_lib:
    temp_list = get_tempkelvin_list(f'{datadir}{sample_name}/')[0]
    # temp_list.pop()
    # kelvin_list = get_tempkelvin_list(f'{datadir}{sample_name}/')[1]
    colorlib = [cmap(i) for i in np.linspace(0,1,len(temp_list))]

    fig = plt.figure(figsize=(5,7), dpi=300)

    y_offset = 0
    for idx in range(len(temp_list)):
        if idx % 3 != 0:                    # reduce the number of curves
            continue
        temp = temp_list[idx]
        workdir = f'{datadir}{sample_name}/{temp}.csv'
        df_raw = get_csv_raw(workdir)
        df_norm = norm_maxdivide(df_raw)
        df = focus_on_range(df_norm, 150)

        x = df.wn.values
        y = df.inten.values + 1.0 * y_offset
        y_offset += 1
        plt.plot(x, y, label=str(temp+273)+' K', color=colorlib[idx], linewidth=1)

    plt.title(fr'Temp-dependent Raman of ({sample_name})$_2$PbI$_4$')
    plt.xlabel(r'Wavenumber (cm)$^{-1}$')
    plt.ylabel('Intensity (a.u.)')
    plt.yticks([])
    plt.legend(loc='center left',bbox_to_anchor=(1.05,0.5))
    plt.savefig(f'../graph/test/{sample_name}_vstack.png', bbox_inches='tight')
    plt.show()




#%% main 2: direct stack
datadir = '../data/0422/'
sample_lib = ['C5', 'PMA', 'R-MBA']
cmap = plt.get_cmap('jet')

for sample_name in sample_lib:
    temp_list = get_tempkelvin_list(f'{datadir}{sample_name}/')[0]
    temp_list.pop()             #discard the degraded sample
    colorlib = [cmap(i) for i in np.linspace(0,1,len(temp_list))]

    fig = plt.figure(figsize=(5,5), dpi=300)

    for idx in range(len(temp_list)):
        # if idx % 3 != 0:                    # reduce the number of curves
        #     continue
        temp = temp_list[idx]
        workdir = f'{datadir}{sample_name}/{temp}.csv'
        df_raw = get_csv_raw(workdir)
        df_norm = norm_maxdivide(df_raw)
        df = focus_on_range(df_norm, 200)

        x = df.wn.values
        y = df.inten.values + 1.0 * y_offset
        plt.plot(x, y, label=str(temp+273)+' K', color=colorlib[idx], linewidth=1)

    plt.title(fr'Temp-dependent Raman of ({sample_name})$_2$PbI$_4$')
    plt.xlabel(r'Wavenumber (cm)$^{-1}$')
    plt.ylabel('Intensity (a.u.)')
    plt.yticks([])
    plt.legend(loc='center left',bbox_to_anchor=(1.05,0.5))
    plt.savefig(f'../graph/0422/{sample_name}_dstack.png', bbox_inches='tight')
    plt.show()


#%% main 3: contour

datadir = '../data/0422/'
sample_lib = ['C5', 'PMA', 'R-MBA']
cmap = plt.get_cmap('jet')

for sample_name in sample_lib:
    temp_list = get_tempkelvin_list(f'{datadir}{sample_name}/')[0].pop()
    kelvin_list = get_tempkelvin_list(f'{datadir}{sample_name}/')[1].pop()

    wnradius = 200

    df_wn_raw = get_csv_raw(f'{datadir}{sample_name}/-195.csv')[['wn']]
    df_wn = focus_on_range(df_wn_raw, wnradius)
    df_all = pd.DataFrame()

    for idx in range(len(temp_list)):
        temp, kelvin = temp_list[idx], kelvin_list[idx]
        df_raw = get_csv_raw(f'{datadir}{sample_name}/{temp}.csv')
        df_norm = norm_maxdivide(df_raw)
        df_temp = focus_on_range(df_norm, wnradius)

        df_all[str(kelvin)] = df_temp['inten']
    
    x = df_wn.wn.values
    y = kelvin_list
    z = df_all.values.T

    fig = plt.figure(figsize=(6,5), dpi=300)
    plt.title(fr'Temp-dependent Raman of ({sample_name})$_2$PbI$_4$')
    plt.xlabel(r'Wavenumber (cm)$^{-1}$')
    plt.ylabel('Temperature (K)')
    plt.contourf(x, y, z, 30, cmap=plt.cm.jet)
    plt.colorbar(label='Intensity (a.u.)')
    plt.savefig(f'../graph/0422/{sample_name}_contour.png')
    plt.show()



#%% same T

for temp in range(-195, 165, 20):
    dirlib = [f'../data/0422/C5/{temp}.csv', f'../data/0422/PMA/{temp}.csv', f'../data/0422/R-MBA/{temp}.csv']

    fig = plt.figure(figsize=(5,5), dpi=300)

    y_offset = 0
    for dir in dirlib:
        df_raw = get_csv_raw(dir)
        df_norm = norm_maxdivide(df_raw)
        df = focus_on_range(df_norm, 150)

        plt.plot(df.wn.values, df.inten.values + 0.9 * y_offset)
        y_offset += 1

    plt.title(f'Raman spectra at {temp} `C')
    plt.savefig(f'../graph/0422/comparison/{temp}.png')
    plt.show()










