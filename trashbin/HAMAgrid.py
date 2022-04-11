# -*- coding: utf-8 -*-

'''===================================='''
'''           [HAMA map gridding]      '''
'''           [Author: CeressGoo]      '''
'''              [2022/03/29]          '''
'''===================================='''

#%% import

import numpy as np
import matplotlib.pyplot as plt
import scipy
from PIL import Image


#%% function

'''=========[function]==================================================================================================='''




#%% main

'''=========[main]==================================================================================================='''

img_raw = Image.open('./data/test1.png')
img = np.array(img_raw)

rows, cols, dims = img.shape

grid_gap = 250

for xcord in range(0, rows, grid_gap):
    for ycord in range(cols):
        img[xcord, ycord, :]=255

for ycord in range(0, cols, grid_gap):
    for xcord in range(rows):
        img[xcord, ycord, :]=255


fig = plt.figure(figsize=(cols, rows), dpi=1)
plt.imshow(img)
plt.axis('off')
plt.savefig('./data/HAMA_grid.png')
plt.show()




