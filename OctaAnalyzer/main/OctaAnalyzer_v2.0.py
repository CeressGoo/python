

'''
=========================================
Perovskite structure analyzer 2.0
by CeressGoo

Added more parameters (Vbasket, inplane/outplane tilt, bondangle variance, bondlen variance, offset)
2022/04/27
=========================================
'''


#%% import 

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utilsfunction as uf

#%% function

'''=============[function start]==========================================================================================='''

def calc_sigma1(datadir):
    sig1_raw = uf.keyword_locate(datadir, 'rawsigma1')
    sig1_res = []

    for octahedral in sig1_raw:
        sig1_ang_list = [float(item.strip()) for item in octahedral.split(',')]
        sig1_ang_arr = np.array(sig1_ang_list)
        sig1_ang_var_arr = (sig1_ang_arr - 90) ** 2
        sig1_2 = np.sum(sig1_ang_var_arr) / 11
        sig1_res.append(sig1_2)

    return sig1_res             # [sigma1, ......]

def calc_sigma2(datadir):
    sig2_raw = uf.keyword_locate(datadir, 'rawsigma2')
    sig2_res = []

    for octahedral in sig2_raw:
        sig2_ang_list = [float(item.strip()) for item in octahedral.split(',')]
        sig2_ang_arr = np.array(sig2_ang_list)
        sig2_ang_var_arr = (sig2_ang_arr - 180) ** 2
        sig2_2 = np.sum(sig2_ang_var_arr) / 2
        sig2_res.append(sig2_2)

    return sig2_res             # [sigma2, ......]

def calc_offset(datadir):
    with open(datadir, 'r', encoding='utf-8') as srcdata:
        block_list = []                     # each block (stored as a list) contains 7 set of coords in a octahedral. block_list is the list of the blocks.
        add_list = []                       
        record_on = False
        for line in srcdata:
            if '/--OS start' in line:
                record_on = True
                continue
            if '/--OS end' in line:
                block_list.append(add_list)
                add_list = []
                record_on = False
                continue
            if record_on and '*' in line:
                # print('Record on, line = ', line.strip())
                coord_str = line.split('*')[1].strip()
                add_list.append(coord_str)

    offset_res = []    
    for block in block_list:
        pb_coord = [float(item.strip()) for item in block[0].strip().split(',')]
        # pb_coord = np.array(pb_coord_list).reshape(1,3)                  # Pb coordination stored in a (1,3) array
        i_coord = np.empty(shape=(0,3))
        for idx in range(1,7,1):
            i_coord_list = [float(item.strip()) for item in block[idx].strip().split(',')]
            i_coord = np.vstack((i_coord, np.array(i_coord_list).reshape(1,3)))
        # so far, 6 I atom coordinations are stored in a (6,3) array
        i_x_avg = np.average(i_coord[:1])
        i_y_avg = np.average(i_coord[:2])
        i_z_avg = np.average(i_coord[:3])

        offset_x = pb_coord[0] - i_x_avg
        offset_y = pb_coord[1] - i_y_avg
        offset_z = pb_coord[2] - i_z_avg
        offset_len = np.sqrt(offset_x ** 2 + offset_y ** 2 + offset_z ** 2)

        offset_val = [offset_x, offset_y, offset_z, offset_len]
        offset_res.append(offset_val)

    return offset_res               # [[offset x, offset y, offset z, offset length], ...]

def calc_lambda(datadir):
    bl_raw = uf.keyword_locate(datadir, 'bondlen')
    bl_res = []
    for octahedral in bl_raw:
        bl_list = [float(item.strip()) for item in octahedral.split(',')]
        bl_arr = np.array(bl_list)
        bl_avg = np.average(bl_arr)
        bl_var = (bl_arr - bl_avg) ** 2
        bl_lambda = np.sum(bl_var) / 6
        bl_res.append([bl_lambda, bl_avg])
    return bl_res               # [[lambda, avg bondlen], ...]

def get_bandgap(datadir):
    bg_raw = uf.keyword_locate(datadir, 'bandgap')[0]
    return float(bg_raw.strip())                # bandgap, float

def get_nbasket(datadir):
    nbas_raw = uf.keyword_locate(datadir, 'basket number')[0]
    return int(nbas_raw.strip())                # number of basket, int

def get_cellparam(datadir):
    param_raw = uf.keyword_locate(datadir, 'Lattice Parameter')[0]
    val_list = [float(item.strip()) for item in param_raw.split(',')]
    a = val_list[0]
    b = val_list[1]
    c = val_list[2]
    alfa = val_list[3]
    beta = val_list[4]
    gama = val_list[5]
    return a, b, c, alfa, beta, gama            # cell parameters

def calc_multiplier(datadir):
    a, b, c, alfa, beta, gama = get_cellparam(datadir)
    nbas = get_nbasket(datadir)
    stack_axis = uf.keyword_locate(datadir, 'stack axis')[0]
    if stack_axis == 'a':
        res = uf.angle_c_to_ab(beta, gama, alfa)
        Sbas = (b * c * math.sin(alfa * math.pi / 180)) / nbas
        axis_l = a
    elif stack_axis == 'b':
        res = uf.angle_c_to_ab(alfa, gama, beta)
        Sbas = (a * c * math.sin(beta * math.pi / 180)) / nbas
        axis_l = b
    elif stack_axis == 'c':
        res = uf.angle_c_to_ab(alfa, beta, gama)
        Sbas = (a * b * math.sin(gama * math.pi / 180)) / nbas
        axis_l = c
    stheta = res[1]
    multiplier = stheta * Sbas * axis_l
    return multiplier                       # float. The multiplier times zdiff to get Vbasket.

def calc_vbasket(datadir):
    nbas = get_nbasket(datadir)
    a, b, c, alfa, beta, gama = get_cellparam(datadir)

    vbas_res = []

    basket_raw = uf.keyword_locate(datadir, 'basket coord')
    for octahedral in basket_raw:
        pb_str = octahedral.strip().split('@')[0]
        i_str = octahedral.strip().split('@')[1]
        pb_coord = [float(item.strip()) for item in pb_str.strip().split(',')]
        i_coord = [float(item.strip()) for item in i_str.strip().split(',')]
        pb_avg = np.sum(pb_coord) / len(pb_coord)
        i_avg = np.sum(i_coord) / len(i_coord)
        zdiff = np.abs(pb_avg - i_avg)                      # z coord difference

        Vbas = zdiff * calc_multiplier(datadir)
        vbas_res.append(Vbas)
    
    return vbas_res                 # [Vbasket, ......]
        
def calc_inplane_angle(datadir):
    ipa_raw = uf.keyword_locate(datadir, 'inplane')[0]
    ipa_list = [float(item.strip()) for item in ipa_raw.strip().split(',')]
    return ipa_list                 # [inplane angle, .....]

def calc_outplane_angle_v(datadir):
    opav_raw = uf.keyword_locate(datadir, 'verticle outplane')[0]
    opav_list = [float(item.strip()) for item in opav_raw.strip().split(',')]
    return opav_list                 # [verticle outplane angle, .....]

def calc_outplane_angle_h(datadir):
    opah_raw = uf.keyword_locate(datadir, 'horizontal outplane')[0]
    opah_list = [float(item.strip()) for item in opah_raw.strip().split(',')]
    return opah_list                 # [horizontal outplane angle, .....]

def generate_report(datadir, savedir):
    print('\n'*3)
    print('='*50)
    print(f'Datadir: {datadir}')
    print(f'Vbasket: {calc_vbasket(datadir)}')
    print(f'inplane angle: {calc_inplane_angle(datadir)}')
    print(f'verticle outplane angle: {calc_outplane_angle_v(datadir)}')
    print(f'horizontal outplane angle: {calc_outplane_angle_h(datadir)}')
    print(f'sigma1: {calc_sigma1(datadir)}')
    print(f'sigma2: {calc_sigma2(datadir)}')
    print(f'Lambda: {calc_lambda(datadir)}')
    print(f'offset: {calc_offset(datadir)}')
    print('='*50)
    with open(savedir, 'w', encoding='utf-8') as rep:
        rep.write(f'Datadir: {datadir}\n')
        rep.write(f'Vbasket: {np.average(calc_vbasket(datadir))}\n')
        rep.write(f'inplane angle: {np.average(calc_inplane_angle(datadir))}\n')
        rep.write(f'verticle outplane angle: {np.average(calc_outplane_angle_v(datadir))}\n')
        rep.write(f'horizontal outplane angle: {np.average(calc_outplane_angle_h(datadir))}\n')
        rep.write(f'sigma1: {np.average(calc_sigma1(datadir))}\n')
        rep.write(f'sigma2: {np.average(calc_sigma2(datadir))}\n')
        rep.write(f'Lambda: {[res[0] for res in calc_lambda(datadir)]}\n')
        rep.write(f'average bondlength: {[res[1] for res in calc_lambda(datadir)]}\n')
        rep.write(f'offset a, b, c: {[reslist[0:3] for reslist in calc_offset(datadir)]}\n')
        rep.write(f'offset length: {[reslist[3] for reslist in calc_offset(datadir)]}')

def generate_namelib(workdir):
    sample_lib = []
    for filename in os.listdir(workdir):
        if '.txt' in filename:
            sample_lib.append(filename.split('.txt')[0])
    return sample_lib           # For file abc.txt, 'abc' is stored in a list (sample_lib)







'''==========[function end]======================================================================================================'''

#%% calc all parameters
# sample_lib = ['PMA_100K', 'PMA_180K', 'PMA_293K', 'rac-MBA_293K', 'C4_223K', 'C4_293K', 'C5_173K', 'C5_293K', 'C5_333K', 'R-MBA_173K', 'S-MBA_173K']

workdir = '../data/TempSpecified/'
sample_lib = generate_namelib(workdir)

# for sample_name in sample_lib:
#     datadir = f'../data/TempSpecified/{sample_name}.txt'
#     repdir = f'../report/tspec/{sample_name}_report.txt'
#     generate_report(datadir, repdir)

vbas_sum = []
ipa_sum = []
opav_sum = []
opah_sum = []
sig1_sum = []
sig2_sum = []
lam_sum = []
blavg_sum = []
offx_sum = []
offy_sum = []
offz_sum = []
offlen_sum = []
bg_sum = []


for sample_name in sample_lib:
    datadir = f'../data/TempSpecified/{sample_name}.txt'
    savedir = f'../report/tspec2/{sample_name}.txt'
    # generate_report(datadir, savedir)

    vbas_sum.append(np.average(calc_vbasket(datadir)))
    ipa_sum.append(np.average(calc_inplane_angle(datadir)))
    opav_sum.append(np.average(calc_outplane_angle_v(datadir)))
    opah_sum.append(np.average(calc_outplane_angle_h(datadir)))
    sig1_sum.append(np.average(calc_sigma1(datadir)))
    sig2_sum.append(np.average(calc_sigma2(datadir)))
    lam_sum.append(np.average([res[0] for res in calc_lambda(datadir)]))
    blavg_sum.append(np.average([res[1] for res in calc_lambda(datadir)]))
    offx_sum.append(np.average([reslist[0] for reslist in calc_offset(datadir)]))
    offy_sum.append(np.average([reslist[1] for reslist in calc_offset(datadir)]))
    offz_sum.append(np.average([reslist[2] for reslist in calc_offset(datadir)]))
    offlen_sum.append(np.average([reslist[3] for reslist in calc_offset(datadir)]))
    bg_sum.append(get_bandgap(datadir))

# print(vbas_sum)
# print(ipa_sum)
# print(opav_sum)
# print(opah_sum)
# print(sig1_sum)
# print(sig2_sum)
# print(lam_sum)
# print(blavg_sum)
# print(offx_sum)
# print(offy_sum)
# print(offz_sum)
# print(offlen_sum)
# print(bg_sum)


#%% plotting

datadic = {
    'V basket': vbas_sum,
    'inplane angle': ipa_sum,
    'verticle outplane angle': opav_sum,
    'horizontal outplane angle': opah_sum,
    'sigma1': sig1_sum,
    'sigma2': sig2_sum,
    'lambda': lam_sum,
    'average bondlength':blavg_sum,
    'offset x': offx_sum,
    'offset y': offy_sum,
    'offset z': offz_sum,
    'offset length': offlen_sum,
    'bandgap': bg_sum
}

x_name = 'average bondlength'
y_name = 'verticle outplane angle'

fig = plt.figure(figsize=(4,4), dpi=300)

x = datadic[x_name]
y = datadic[y_name]

plt.scatter(x, y, color='red', marker='o', s=15)
for idx in range(len(x)):
    plt.annotate(sample_lib[idx], xy=(x[idx], y[idx]), fontsize=6)

plt.title(f'{x_name} - {y_name}')
plt.xlabel(f'{x_name}')
plt.ylabel(f'{y_name}')
# plt.savefig(f'../graph/20220430/{x_name} - {y_name}.png', bbox_inches='tight')
plt.show()





#%% generate report for single sample

workdir = '../data/TempSpecified/'
sample_name = 'S-4BrMBA_199K'
datadir = f'../data/TempSpecified/{sample_name}.txt'
savedir = f'../report/tspec2/{sample_name}.txt'
generate_report(datadir, savedir)












#%%

print(generate_namelib('../data/TempSpecified'))







#%% C5 333K expolation

x = 333
res = -0.000000017179615 * (x ** 3) + 0.000006925739673 * (x ** 2) - 0.001112257959129 * x + 2.598264901509160
print(res)




#%% test1

a, b, c = [1,2,3], [2,3,4], [3,4,5]

srcdic = {
    'p1': a,
    'p2': b,
    'p3': c
}

x = srcdic['p1']

print(x[1], type(x))









































# %%
