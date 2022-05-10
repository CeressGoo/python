



#%% import

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model


#%% function





#%% main

dataset = {'basis':['cc-pvtz', 'cc-pvqz', 'cc-pv5z', 'cc-pv6z'], 
            'L':[3,4,5,6], 
            'E':[-1.13254516245,-1.13302771162,-1.13317248647,-1.13318949556]}
df = pd.DataFrame(dataset)
df['exp_L'] = np.exp(-df.L.values)

x = df.exp_L.values.reshape(-1,1)
y = df.E.values.reshape(-1,1)

reg_model = linear_model.LinearRegression()
reg_model.fit(x, y)
intcpt = reg_model.intercept_[0]
slp = reg_model.coef_[0][0]

x_plot = np.linspace(0,0.05,100).reshape(-1,1)
y_pred = reg_model.predict(x_plot)

fig = plt.figure(figsize=(5,5), dpi=300)
plt.scatter(x, y, color='red', s=30, marker='x', label='Calculation')
plt.plot(x_plot, y_pred, color='blue', linewidth=1, label='Fit result')
plt.legend()

plt.xlabel(r'exp(-L)')
plt.ylabel('Energy (Hartree)')
plt.title('Calculation and fit results of different basis')
plt.text(x=0.015, y=-1.13315, s=r'E = %.7f + %.7f exp$^{-L}$' % (intcpt, slp))

plt.savefig('QChemw1_fit.png', bbox_inches='tight')
plt.show()


#%% calc

ecorr = -200.029545809033
e_abab = -200.030753501
e_aab = -100.012803907
e_bab = -100.011777709
e_aa = -100.011688982
e_bb = -100.011684942

bsse = e_aa - e_aab + e_bb -e_bab
comp_corr = e_abab - e_aab - e_bab
comp = e_abab - e_aa - e_bb

print('bsse: %.9f' % bsse)
print('comp_corr: %.9f' % comp_corr)
print('comp: %.9f' % comp)

print(ecorr - e_abab)


































