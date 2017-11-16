import numpy as np
import sys
import time

from setting import Setting
from clock import Clock

def initial_pos(r):
    return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)*np.sin(r[2]*2*np.pi)

type = sys.argv[1]

if type == 'qtt':
    from qtt_data import QTTData as Data
elif type == 'sparse':
    from sparse_data import SparseData as Data
else:
    exit

current_time = time.strftime("20%y%d%m_%T")
setting = Setting(n=6, dim=3, tau=1e-4, tol=1e-4, max_T=0.5, rmax=10, result_dir='3D/{}/{}'.format(type, current_time))

data = Data(setting, initial_pos)


with Clock(output_path=setting.result_path()) as clock:
    for i in range(setting.max_iter):
        data.next_step()
        if i%(setting.max_iter/9) == 0:
            data.write()

        if i%100 == 0:
            data.energy_calc()

        if i == setting.max_iter-1:
            data.write()
