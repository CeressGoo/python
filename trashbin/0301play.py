#%%

import numpy as np

#%%
x = np.array([[4,-5], [-2,1]])

print(x)

#%%
eigvalue, eigvec = np.linalg.eig(x)
print(f'eigval = {eigvalue}')
print(f'eigvec = {eigvec}')





