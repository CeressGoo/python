# -*- coding: utf-8 -*-

'''===================================='''
'''        [APbX3 Pb-offset calc]      '''
'''         [Author: CeressGoo]        '''
'''            [2022/03/30]            '''
'''===================================='''

import numpy as np
import pandas as pd


I_coord = pd.DataFrame(columns=['x', 'y', 'z'])

for Inum in range(6):
    print('*'*50)
    x_I = float(input(f'F atom {Inum+1} x coordination: '))
    y_I = float(input(f'F atom {Inum+1} y coordination: '))
    z_I = float(input(f'F atom {Inum+1} z coordination: '))
    print('*'*50)
    new_I = pd.DataFrame({'x':x_I, 'y':y_I, 'z':z_I}, index=[Inum+1])
    I_coord = I_coord.append(new_I, ignore_index=True)

print('*'*50)
x_Pb = float(input('Pb atom 1 x coordination: '))
y_Pb = float(input('Pb atom 1 y coordination: '))
z_Pb = float(input('Pb atom 1 z coordination: '))
print('*'*50)
Pb_coord = np.array([x_Pb, y_Pb, z_Pb])

I_center = np.array([I_coord.x.mean(), I_coord.y.mean(), I_coord.z.mean()])

offset = Pb_coord - I_center
offset_length = np.sqrt((offset[0] ** 2) + (offset[1] ** 2) + (offset[2] ** 2))
print('offset:\n', offset)
print('offset length: ', offset_length)





