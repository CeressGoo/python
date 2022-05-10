# -*- coding: utf-8 -*-

'''
=====================================
           [utilities]
        [Author: CeressGoo]
            [2022/04/08]
=====================================
'''


#%% import

import math
import numpy as np


#%% function

def angle_c_to_ab(alfa_r, beta_r, gama_r):
    alfa = alfa_r * (2*math.pi / 360)
    beta = beta_r * (2*math.pi / 360)
    gama = gama_r * (2*math.pi / 360)
    ca = math.cos(alfa)
    cb = math.cos(beta)
    cy = math.cos(gama)
    ctheta = math.sqrt(ca**2 + cb**2  - 2*ca*cb*cy) / math.sin(gama)
    stheta = math.sqrt(1 - ctheta**2)
    return [ctheta, stheta]

def vbasket_pbi(a, b, c, alfa, beta, gama, zavg_pb, zavg_i, n_basket):
    s_basket = (a * b * math.sin(2*math.pi*gama / 360)) / n_basket
    zavg_diff = math.fabs(zavg_pb - zavg_i)
    sin_c_ab = angle_c_to_ab(alfa, beta, gama)[1]
    return s_basket * zavg_diff * sin_c_ab

def keyword_locate(datadir, kwd):
    with open(datadir, 'r', encoding='utf-8') as src:
        res = []
        for line in src:
            if kwd in line:
                val = line.split('/*')[1].strip()
                res.append(val)
    return res

def read_data(datadir):
    with open(datadir, 'r', encoding='utf-8') as f:
        block_list = []         # chop the raw data text into several blocks: 1. parameters; 2~n: PbI basket coords
        add_list = []
        for line in f:
            if '/--' in line:                   # start a new block once the line contains '/--'
                block_list.append(add_list)
                add_list = []
            if line.strip() == '':                      # discard empty lines
                continue
            add_list.append(line)
        block_list.append(add_list)             # saving the last block
        block_list.pop(0)                       # discard the first element, because it's the head lines before /--block1.
    return block_list

def calc_bondlen(block_list):
    oct_list = []
    for block in block_list:
        bl_list = []
        for line in block:
            if '=' not in line:
                continue
            line_latter = line.split('=')[1].strip()
            bl_number_str = line_latter.split('(')[0].strip()
            bl_number = float(bl_number_str)
            bl_list.append(bl_number)
        oct_property = [np.mean(bl_list), np.std(bl_list)]
        oct_list.append(oct_property)
    return oct_list                     # oct_list contains all the [avg bondlen, std bondlen] pair for each octahedral in a list.

def calc_avg_bondlen(block_list):
    oct_list = calc_bondlen(block_list)
    avg_bondlen = np.mean([bondlen for [bondlen, bl_std] in oct_list])
    return avg_bondlen

def calc_avg_std(block_list):
    oct_list = calc_bondlen(block_list)
    avg_std = np.mean([bl_std for [bondlen, bl_std] in oct_list])
    return avg_std





#%% main
def main():
    # datadir = '../data/bondlen/template.txt'

    # block_list = read_data(datadir)

    # oct_list = calc_bondlen(block_list)

    # avg_bl = calc_avg_bondlen(block_list)

    # print(avg_bl)

    # print(angle_c_to_ab(90,95,90))
    # print(np.sin(95 * math.pi / 180))


    print(keyword_locate('../data/TempSpecified/template.txt', 'sigma2'))


if __name__ == '__main__':
    main()


