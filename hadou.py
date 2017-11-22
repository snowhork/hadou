import numpy as np
import sys
import time

from setting import Setting
from clock import Clock

def initial_pos(r):
    return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)*np.sin(r[2]*2*np.pi)

def initial_pos2(r):
    return np.sin(r[0]*np.pi)*np.sin(r[1]*np.pi)*np.sin(r[2]*np.pi)

def initial_pos2D(r):
    return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)

def initial_pos1D(r):
    return np.sin(r*2*np.pi)

type = sys.argv[1]

write = True
if len(sys.argv) > 2 and sys.argv[2] == 'nowrite':
    write = False

if type == 'qtt':
    from qtt_data import QTTData as Data
elif type == 'sparse':
    from sparse_data import SparseData as Data
elif type == 'sparse1D':
    from sparse1D_data import Sparse1DData as Data
elif type == 'sparse2D':
    from sparse2D_data import Sparse2DData as Data
else:
    exit

current_time = time.strftime("20%y%d%m_%T")
setting = Setting(n=6, dim=2, tau=1e-4, tol=1e-4, max_T=1, rmax=10, result_dir='{}/{}'.format(type, current_time))

data = Data(setting, initial_pos2D)

with Clock(output_path=setting.result_path()) as clock:
    for i in range(setting.max_iter):
        data.next_step()
        if i%(setting.max_iter/8) == 0 and write:
            data.write()
            print("{}: write.".format(i))

        if i%100 == 0:
            data.energy_calc()

data.write()
print("result_path: {}".format(setting.result_path()))

