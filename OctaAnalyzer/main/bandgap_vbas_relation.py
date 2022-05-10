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
from sklearn.preprocessing import PolynomialFeatures



#%% function
def linear_regression(vbas_all, bg_all):
    reg_model = linear_model.LinearRegression()
    reg_model.fit(vbas_all, bg_all)
    bg_pred = reg_model.predict(vbas_all)
    plt.plot(vbas_all, bg_pred, color='gray')
    return bg_pred


def polynomial_regression(vbas_all, bg_all):
    poly_model = linear_model.LinearRegression()
    poly_featurizer = PolynomialFeatures(degree=2)
    vbas_transform = poly_featurizer.fit_transform(vbas_all)
    poly_model.fit(vbas_transform, bg_all)
    vbas_plotting = np.linspace(min(vbas_all), max(vbas_all), 100).reshape(-1,1)
    vbas_plotting_transform = poly_featurizer.transform(vbas_plotting)
    bg_plot = poly_model.predict(vbas_plotting_transform)
    plt.plot(vbas_plotting, bg_plot, linewidth=1, color='grey')

    bg_pred = poly_model.predict(vbas_transform)
    return bg_pred




#%% main
df = pd.read_csv('../data/bandgap/bandgap_all2.csv')

sample_lib = ['PMA', '4FPMA', '4ClPMA', '4BrPMA', 'PEA', '4FPEA', '4ClPEA', '4BrPEA', 'R-MBA', 'S-MBA', 'rac-MBA', 'BA']
# sample_lib = ['PMA', '4FPMA', '4ClPMA', '4BrPMA', 'PEA', '4FPEA', '4ClPEA', '4BrPEA']


fig = plt.figure(figsize=(6,5), dpi=300)

for sample_name in sample_lib:
    bg = df[df['name'] == sample_name].bg.values
    vbas = df[df['name'] == sample_name].vbas.values
    plt.scatter(vbas, bg, label=sample_name)
    print(f'{sample_name} done: {bg} {vbas}')

bg_all = df.bg.values.reshape(-1,1)
vbas_all = df.vbas.values.reshape(-1,1)

bg_pred = polynomial_regression(vbas_all, bg_all)

# rmse = metrics.mean_squared_error(bg_pred, bg_all, squared=True)
# plt.text(119, 2.37, f'RMSE = {rmse}')

plt.title('Bandgap-V_basket Relationship')
plt.xlabel(r'V_basket (A${^3}$)')
plt.ylabel('Bandgap (eV)')
plt.legend(bbox_to_anchor=(1.3,0.8))
plt.savefig('../graph/bg-vbas_relation_polyreg_n.png', bbox_inches='tight')
# plt.savefig('../graph/bg-vbas_relation.png')
plt.show()
















