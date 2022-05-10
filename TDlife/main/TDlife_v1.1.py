# -*- coding:utf-8 -*-

'''
*************************************************
Temperature-dependent lifetime analysis tool
by CeressGoo
2022.04.17
*************************************************
'''

#%% import 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% function

def get_txt(datadir):
    df = pd.read_table(datadir, header=None, names=['t', 'tau'])
    return df





#%% main 1
sample_lib = ['PMA', '4FBzA']
workdir = '../data/'
colorlib = ['blue', 'red']

idx = 0
for sample_name in sample_lib:
    datadir = f'{workdir}{sample_name}.txt'
    df = get_txt(datadir)
    kelvin = df.t.values + 273
    tau = df.tau.values

    #log plot
    fig = plt.figure(figsize=(5,5), dpi=300)
    plt.plot(kelvin, -np.log(tau), color=colorlib[idx], label=sample_name)
    plt.title(fr'TDlife results of ({sample_name})$_2$PbI$_4$')
    plt.xlabel('Temperature (K)')
    plt.ylabel(r'ln(1/$\tau$)')
    plt.xscale('log')
    plt.xticks([100,200,300,400], ['100', '200', '300', '400'])
    plt.legend()
    plt.savefig(f'../graph/{sample_name}_log.png')
    plt.show()

    #linear plot
    fig = plt.figure(figsize=(5,5), dpi=300)
    plt.plot(kelvin, tau, color=colorlib[idx], label=sample_name)
    plt.title(fr'TDlife results of ({sample_name})$_2$PbI$_4$')
    plt.xlabel('Temperature (K)')
    plt.ylabel(r'Lifetime ($\tau$)')
    # plt.xticks([100,200,300,400], ['100', '200', '300', '400'])
    plt.legend()
    plt.savefig(f'../graph/{sample_name}_lin.png')
    plt.show()

    idx += 1


















