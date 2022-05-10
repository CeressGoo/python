#%%
import numpy as np


#%% func

def keyword_locate(srcdata, kwd):
    res = []
    for line in srcdata:
        if kwd in line:
            val = line.split('/*')[1].strip()
            res.append(val)
    return res





#%%
with open('source.txt', 'r', encoding='utf-8') as src:
    res = keyword_locate(src, 'multival')
    print(res)