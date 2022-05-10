# -*- coding: utf-8 -*-

'''======================================'''
'''   [Perovskite octahedral analyzer]   '''
'''        [Author: CeressGoo]           '''
'''           [2022/04/07]               '''
'''======================================'''




#%% import

import math
from utilsfunction import angle_c_to_ab


#%% function

'''===========[function]===================================================================='''
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

def calc_zavg(block):
    line_pb, line_i = block[1], block[2]
    zlist_pb, zlist_i = [], []
    coord_pb = line_pb.split(':')[1].strip()
    coord_i = line_i.split(':')[1].strip()

    for val in coord_pb.split(','):
        zlist_pb.append(float(val))
    for val in coord_i.split(','):
        zlist_i.append(float(val))

    zavg_pb = sum(zlist_pb) / len(zlist_pb)
    zavg_i = sum(zlist_i) / len(zlist_i)

    return [abs(zavg_pb - zavg_i), zavg_pb, zavg_i]

def calc_havg(block, axis_h):
    line_pb, line_i = block[1], block[2]
    zlist_pb, zlist_i = [], []
    coord_pb = line_pb.split(':')[1].strip()
    coord_i = line_i.split(':')[1].strip()

    for val in coord_pb.split(','):
        zlist_pb.append(float(val))
    for val in coord_i.split(','):
        zlist_i.append(float(val))

    zavg_pb = sum(zlist_pb) / len(zlist_pb)
    zavg_i = sum(zlist_i) / len(zlist_i)

    return [abs(zavg_pb - zavg_i)*axis_h, zavg_pb*axis_h, zavg_i*axis_h]


def parameter_definition(bl):
    a = float(bl[1].split(':')[1].strip())
    b = float(bl[2].split(':')[1].strip())
    c = float(bl[3].split(':')[1].strip())
    alfa = float(bl[4].split(':')[1].strip())
    beta = float(bl[5].split(':')[1].strip())
    gama = float(bl[6].split(':')[1].strip())
    n_basket = float(bl[7].split(':')[1].strip())
    return a, b, c, alfa, beta, gama, n_basket




#%% main 1: verticle axis = c, absolute coord input files

'''==========[main]========================================================================='''

sample_name = '4ClPMA_1'
datadir = f'../data/PMAseries/{sample_name}.txt'
bl_list = read_data(datadir)

a, b, c, alfa, beta, gama, n_basket = parameter_definition(bl_list[0])

V_bas_list = []

with open(f'../report/{sample_name}.txt', 'w', encoding='utf-8') as rep:
    print(f'======{sample_name}======')
    for block in bl_list[1:]:
        zdiff = calc_zavg(block)[0]
        S_basket = (a * b * math.sin(gama * math.pi / 180)) / n_basket
        stheta = angle_c_to_ab(alfa, beta, gama)[1]
        V_basket = S_basket * zdiff * stheta

        V_bas_list.append(V_basket)

        # print(f'\nSbas = {S_basket}, zdiff = {zdiff}, stheta = {stheta}')
        print('Vbas = %.5f' % V_basket)

        rep.write(f'\nSbas = {S_basket}, zdiff = {zdiff}, stheta = {stheta}')
        rep.write('\nVbas = %.5f \n' % V_basket)
    
    rep.write('\n\nAverage Volume of PbI basket: %.5f' % (sum(V_bas_list) / len(V_bas_list)))


#%% main 2: verticle axis = a, relative coord input files

sample_name = '4FPEA_1'
datadir = f'../data/PEAseries/{sample_name}.txt'
bl_list = read_data(datadir)

a, b, c, alfa, beta, gama, n_basket = parameter_definition(bl_list[0])

V_bas_list = []

with open(f'../report/{sample_name}.txt', 'w', encoding='utf-8') as rep:
    print(f'======{sample_name}======')
    for block in bl_list[1:]:
        zdiff = calc_havg(block, a)[0]
        S_basket = (c * b * math.sin(alfa * math.pi / 180)) / n_basket
        stheta = angle_c_to_ab(gama, beta, alfa)[1]
        V_basket = S_basket * zdiff * stheta

        V_bas_list.append(V_basket)

        # print(f'\nSbas = {S_basket}, zdiff = {zdiff}, stheta = {stheta}')
        print('Vbas = %.5f' % V_basket)

        rep.write(f'\nSbas = {S_basket}, zdiff = {zdiff}, stheta = {stheta}')
        rep.write('\nVbas = %.5f \n' % V_basket)
    
    rep.write('\n\nAverage Volume of PbI basket: %.5f' % (sum(V_bas_list) / len(V_bas_list)))


#%% main 3: verticle axis = c, relative coord input files

sample_name = 'rac-MBA_1'
datadir = f'../data/MBAseries/{sample_name}.txt'
bl_list = read_data(datadir)

a, b, c, alfa, beta, gama, n_basket = parameter_definition(bl_list[0])

V_bas_list = []

with open(f'../report/{sample_name}_test.txt', 'w', encoding='utf-8') as rep:
    print(f'======{sample_name}======')
    for block in bl_list[1:]:
        zdiff = calc_havg(block, c)[0]
        S_basket = (a * b * math.sin(gama * math.pi / 180)) / n_basket
        stheta = angle_c_to_ab(alfa, beta, gama)[1]
        V_basket = S_basket * zdiff * stheta
        print(f'sbas: {S_basket}, zdiff: {zdiff}, stheta:{stheta}')

        V_bas_list.append(V_basket)

        # print(f'\nSbas = {S_basket}, zdiff = {zdiff}, stheta = {stheta}')
        print('Vbas = %.5f' % V_basket)

        rep.write(f'\nSbas = {S_basket}, zdiff = {zdiff}, stheta = {stheta}')
        rep.write('\nVbas = %.5f \n' % V_basket)
    
    rep.write('\n\nAverage Volume of PbI basket: %.5f' % (sum(V_bas_list) / len(V_bas_list)))













# %%
