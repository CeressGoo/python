# -*- coding: utf-8 -*-

'''======================================'''
'''  [bandgap-Vbasket relation analyse]  '''
'''        [Author: CeressGoo]           '''
'''           [2022/04/10]               '''
'''======================================'''




#%% import

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model, metrics



#%% function



#%% main
df = pd.read_csv('../data/bandgap/bandgap_all.csv')

sample_lib = ['PMA', '4FPMA', '4ClPMA', '4BrPMA', 'PEA', '4FPEA', '4ClPEA', '4BrPEA', 'R-MBA', 'S-MBA', 'rac-MBA']


fig = plt.figure(figsize=(6,5), dpi=300)

for sample_name in sample_lib:
    bg = df[df['name'] == sample_name].bg.values
    vbas = df[df['name'] == sample_name].vbas.values
    plt.scatter(vbas, bg, label=sample_name)
    print(f'{sample_name} done')

bg_all = df.bg.values.reshape(-1,1)
vbas_all = df.vbas.values.reshape(-1,1)

reg_model = linear_model.LinearRegression()
reg_model.fit(vbas_all, bg_all)

bg_pred = reg_model.predict(vbas_all)

slope = reg_model.coef_[0,0]
intercept = reg_model.intercept_[0]
rmse = metrics.mean_squared_error(bg_pred, bg_all, squared=True)

print(slope, intercept)


plt.plot(vbas_all, bg_pred, color='gray')
plt.text(107.5,2.435, 'E = %.5fV + %.3f' % (slope, intercept))

plt.title('Bandgap-V_basket Relationship')
plt.xlabel(r'V_basket (A${^3}$)')
plt.ylabel('Bandgap (eV)')
plt.legend(bbox_to_anchor=(1.3,0.8))
plt.savefig('../graph/bg-vbas_relation.png')
plt.show()
















