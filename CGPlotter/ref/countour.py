'''=============================='''
'''       Date: 2022/03/14       '''
'''     TDPL countour figure     '''
'''      Author: Ceress Goo      '''
'''=============================='''


#%% imports

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



#%% functions
'''==========================[function]=================================================================='''
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




#%% main
'''===========================[main]========================================================================='''
sample_name = '4ClBzA'
datadir = f'../data/{sample_name}/'
temp_list = list(range(-195, 105, 15))
graphdir = '../graph/test2/countour/'

# working modes: select range (true) / all range (false)
select_range = True


# generating wavelength row
if select_range:
    centerwl = 525
    rangewidth = 80
    df_0_raw = pd.read_csv(datadir+'-195.csv', header=None, names=['wl', 'inten'])
    df_0 = data_sel_range(df_0_raw, centerwl, rangewidth)['wl']
else:
    df_0 = pd.read_csv(datadir+'-195.csv', header=None, names=['wl', 'inten'])['wl']
df_all = df_0.to_frame()                # create a column of wavelength using the -195 data

temp_name_list = []
kelvin_list = []

for temp in temp_list:
    if os.path.exists(datadir+f'{temp}.csv'):
        df_norm = get_data_normed(datadir, temp)
        if select_range:
            df_selrange = data_sel_range(df_norm, centerwl, rangewidth)
            df_all[str(temp+273)] = df_selrange['inten']
        else:
            df_all[str(temp+273)] = df_norm['inten']            
        temp_name_list.append(str(temp+273))
        kelvin_list.append(temp+273)
# by now, all data for this sample is stored in df_all.
# the first row is wavelength, the other rows are intensities, and the row name is the temp(in kelvin)

inten = df_all[temp_name_list].values.T     #get all intensity data for plotting

#% plotting

fig = plt.figure(figsize=(6,5), dpi=300)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Temperature (K)')
plt.title(fr'TDPL Spectrum of ({sample_name})$_2$PbI$_4$')
plt.contourf(df_all['wl'].values, kelvin_list, inten, 20, cmap=plt.cm.jet)
plt.colorbar()
if select_range:
    plt.savefig(graphdir+f'{sample_name}-zoom.png')
else:
    plt.savefig(graphdir+f'{sample_name}.png')
plt.show()










#%% plgnd
'''==========================[playground]======================================================================'''

x = np.linspace(0,10,100)
y = np.linspace(0,10,100)
t = np.linspace(0,10,100)

x1, y1 = np.meshgrid(x, y)

z1 = x1 + y1

df = pd.DataFrame({'x':x, 'y':y, 't':t})

data = df[['x', 'y']].values
# print(data, type(data))













