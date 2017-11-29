import numpy as np
import sys
import time

from setting import Setting
from clock import Clock

def initial_pos3D(r):
    return 4*np.arctan(np.exp(3-14*np.sqrt((r[0]-0.5)**2 + (r[1]-0.5)**2 + (r[2]-0.5)**2)))

def initial_pos2D(r):
    return 4*np.arctan(np.exp(3-14*np.sqrt((r[0]-0.5)**2 + (r[1]-0.5)**2)))

type = sys.argv[1]

write = True
if len(sys.argv) > 2 and sys.argv[2] == 'nowrite':
    write = False

dim = 3
initial_pos = initial_pos3D
if type == 'qtt3D':
    from data.qtt_data import QTTData as Data
    from sine_gordon_scheme.sine_qtt import SineQTTScheme as Scheme
elif type == 'sparse3D':
    from data.sparse_data import SparseData as Data
    from sine_gordon_scheme.sine_sparse import SineSparseScheme as Scheme
elif type == 'sparse2D':
    from data.sparse_data import SparseData as Data
    from sine_gordon_scheme.sine_sparse import SineSparseScheme as Scheme
    initial_pos = initial_pos2D

    dim = 2
else:
    exit

current_time = time.strftime("20%y%d%m_%T")

# 1.0/np.sqrt(3)/2.0 = 0.28867513459481292
setting = Setting(n=7, dim=dim, tau=1e-6, tol=1e-4, max_T=0.02, rmax=10000, result_dir='sine/{}/{}'.format(type, current_time))

data = Data(setting, initial_pos)

class Calcurator(Data, Scheme):
    def __init__(self, setting, initial_pos, neumann=False):
        super(Calcurator, self).__init__(setting, initial_pos, neumann)
        self.initial_step()


calc = Calcurator(setting, initial_pos)

with Clock(output_path=setting.result_path()) as clock:
    for i in range(setting.max_iter):
        calc.next_step()
        if i%(setting.max_iter/8) == 0 and write:
            calc.write()

        if i%100 == 0:
            calc.show()

calc.write()
print("result_path: {}".format(setting.result_path()))

