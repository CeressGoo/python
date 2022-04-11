'''========================================='''
'''       [CeressGoo Plotter v0.2]          '''
'''         [Python cell version]           '''
'''========================================='''


#%% import

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% function
def get_csv_raw(datadir):
    df = pd.read_csv(datadir, header=None, names=['wl', 'inten'])
    return df

def get_txt_raw(datadir):
    df = pd.read_table(datadir, header=None, names=['wl', 'inten'])
    return df

def norm_df(df):
    max_inten = df.inten.values.max()
    df_n = df[['wl', 'inten']]
    df_n.inten = df.inten / max_inten
    return df_n

def add_line(df, setname):
    wl = df.wl.values
    inten = df.inten.values
    plt.plot(wl, inten, label=setname)

#%% main 1

# work mode selection
sourcetype = 'csv'
norm_select = True          # True = normalization, False = don't normalize
sample_name = 'PEA series'

# generate datafile directory list
workdir = '../data/'
dirlib = os.listdir(workdir)

# initialize the graph
fig = plt.figure(figsize=(5,5), dpi=300)

# plot every set of data onto the graph
for datadir in dirlib:
    # generate correct dataframe
    if sourcetype == 'txt':
        df_raw = get_txt_raw(workdir+datadir)
    elif sourcetype == 'csv':
        df_raw = get_csv_raw(workdir+datadir)
    else:
        break
    # determine whether normalization is needed
    if norm_select:
        df_work = norm_df(df_raw)
    else:
        df_work = df_raw
    # add a set of data onto the graph
    setname = datadir[:-4]
    add_line(df_work, setname)
    # generate report
    max_value = df_work.inten.values.max()
    df_max = df_work[df_work['inten'] == max_value]
    peak_wl = df_max['wl'].values[0]
    max_inten = df_raw[df_raw['wl'] == peak_wl].inten.values[0]
    with open(f'../report/{datadir[:-4]}.txt', 'w', encoding='utf-8') as rep:
        rep.write(f'Peak wavelength: {peak_wl} nm\n')
        rep.write(f'Max intensity: {max_inten}')
        
        
# show and save the fig
plt.title(sample_name)
plt.legend()
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (a.u.)')
plt.savefig(f'../graph/{sample_name}.png', bbox_inches='tight')
plt.show()


























