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





