import numpy as np
import sys
import time

from setting import Setting
from clock import Clock

def initial_pos3D(r):
    return (np.sin(r[0]*np.pi)**4)*(np.sin(r[1]*np.pi)**4)*(np.sin(r[2]*np.pi)**2)

# def initial_pos2D(r):
#     return 4*np.arctan(np.exp(3-14*np.sqrt((r[0]-0.5)**2 + (r[1]-0.5)**2)))

def initial_pos2D(r):
    return (np.sin(r[0]*np.pi)**4)*(np.sin(r[1]*np.pi)**4)

type = sys.argv[1]
n = int(sys.argv[2])

write = True
if len(sys.argv) > 3 and sys.argv[3] == 'nowrite':
    write = False

inspect = False
if len(sys.argv) > 3 and sys.argv[3] == 'inspect':
    write = False
    inspect = True

if len(sys.argv) > 3 and sys.argv[3] == 'write-inspect':
    write = True
    inspect = True


file_name = time.strftime("20%y%d%m_%T")
if len(sys.argv) > 4:
    file_name = sys.argv[4]


tol = 1e-4
if len(sys.argv) > 5 and sys.argv[5] == 'tol6':
    tol = 1e-6
if len(sys.argv) > 5 and sys.argv[5] == 'tol8':
    tol = 1e-8


dim = 3
initial_pos = initial_pos3D
if type == 'qtt2D-cn':
    from data.qtt_data_cn import QTTDataCN as Data
    from sine_gordon_scheme.sine_qtt_cn import SineQTTCNScheme as Scheme
    initial_pos = initial_pos2D
    dim = 2
elif type == 'qtt3D-cn':
    from data.qtt_data_cn import QTTDataCN as Data
    from sine_gordon_scheme.sine_qtt_cn import SineQTTCNScheme as Scheme
    initial_pos = initial_pos3D
elif type == 'qtt3D':
    from data.qtt_data_cn import QTTDataCN as Data
    from sine_gordon_scheme.sine_qtt import SineQTTScheme as Scheme
    initial_pos = initial_pos3D
elif type == 'qtt3D-cn-deim':
    from data.qtt_data_cn import QTTDataCN as Data
    from sine_gordon_scheme.sine_qtt_cn_deim import SineQTTCNSchemeDEIM as Scheme
    initial_pos = initial_pos3D
elif type == 'qtt3D-cn-deim2':
    from data.qtt_data_cn import QTTDataCN as Data
    from sine_gordon_scheme.sine_qtt_cn_deim2 import SineQTTCNSchemeDEIM2 as Scheme
    initial_pos = initial_pos3D
elif type == 'sparse3D':
    from data.sparse_data import SparseData as Data
    from sine_gordon_scheme.sine_sparse import SineSparseScheme as Scheme
elif type == 'sparse2D':
    from data.sparse_data import SparseData as Data
    from sine_gordon_scheme.sine_sparse import SineSparseScheme as Scheme
    initial_pos = initial_pos2D

    dim = 2
elif type == 'sparse2D-cn':
    from data.sparse_data_cn import SparseDataCN as Data
    from sine_gordon_scheme.sine_sparse_cn import SineSparseCNScheme as Scheme
    initial_pos = initial_pos2D
    dim = 2
elif type == 'sparse3D-cn':
    from data.sparse_data_cn import SparseDataCN as Data
    from sine_gordon_scheme.sine_sparse_cn import SineSparseCNScheme as Scheme
    initial_pos = initial_pos3D
else:
    exit

current_time = time.strftime("20%y%d%m_%T")

# 1.0/np.sqrt(3)/2.0 = 0.28867513459481292
setting = Setting(n=n, dim=dim, tau=5e-3, tol=tol, max_T=6, rmax=10000, result_dir='sine/{}/{}'.format(type, file_name))

data = Data(setting, initial_pos)

class Calcurator(Data, Scheme):
    def __init__(self, setting, initial_pos, neumann=False):
        super(Calcurator, self).__init__(setting, initial_pos, neumann)
        self.initial_step()


calc = Calcurator(setting, initial_pos)

print(setting.result_path())
print("n: " + str(setting.n))
print("tol: " + str(setting.tol))
with Clock(output_path=setting.result_path()) as clock:
    for i in range(setting.max_iter):
        calc.next_step()

        if inspect and i%10 == 0:
            calc.info()
            print("step: " + str(i) + " time: " + str(clock.current))

        if i%(setting.max_iter/8) == 0 and write:
            calc.write()

        if i%100 == 0:
            calc.show()
            print("step: " + str(i) + " time: " + str(clock.current))


if inspect:
    calc.info_write()
else:
    calc.write()
print(setting.result_path())

