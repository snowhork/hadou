import numpy as np
import sys
import time

from setting import Setting
from clock import Clock

# def initial_pos3D(r):
#     return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)*np.sin(r[2]*2*np.pi)
def initial_pos2D_yama(r):
    return np.arctan(np.exp(3-14*np.sqrt((r[0]-0.5)**2 + (r[1]-0.5)**2)))


def initial_pos3D(r):
    return (np.sin(r[0]*np.pi)**4)*(np.sin(2*r[1]*np.pi)**4)*(np.sin(r[2]*np.pi))


# def initial_pos3D(r):
#     x = 0
#     if r[0] <= 0.8:
#         x = -np.abs(0.4-r[0]) + 0.4
#         x *= 1/0.4

#     y = 0
#     if r[1] <= 0.8:
#         y = -np.abs(0.4-r[1]) + 0.4
#         y *= 1/0.4

#     z = 0
#     if r[2] <= 0.8:
#         z = -np.abs(0.4-r[2]) + 0.4
#         z *= 1/0.4


#     return x*y*z

def initial_pos_kukei(r):
    x = 0
    if r[0] <= 0.75 and r[0] >= 0.25:
        x = 1

    y = 0
    if r[1] <= 0.75 and r[1] >= 0.25:
        y = 1

    z = 0
    if r[2] <= 0.75 and r[2] >= 0.25:
        z = 1

    return x*y*z


# def initial_pos2(r):
#     return np.sin(r[0]*np.pi)*np.sin(r[1]*np.pi)*np.sin(r[2]*np.pi)

def initial_pos2D(r):
    return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)

def initial_pos1D(r):
    return np.sin(r*2*np.pi)

def initial_pos_kukei1D(r):
    if r[0] <= 0.75 and r[0] >= 0.25:
        return 0.9
    return 0.0


type = sys.argv[1]
n = int(sys.argv[2])

write = True
if len(sys.argv) > 3 and sys.argv[3] == 'nowrite':
    write = False

inspect = False
if len(sys.argv) > 3 and sys.argv[3] == 'inspect':
    write = False
    inspect = True


file_name = time.strftime("20%y%d%m_%T")
if len(sys.argv) > 4:
    file_name = sys.argv[4]

dim = 3
initial_pos = initial_pos3D
if type == 'qtt3D':
    from data.qtt_data import QTTData as Data
    from hadou_scheme.hadou_qtt import HadouQTTScheme as Scheme
elif type == 'qtt2-3D':
    from data.qtt2_data import QTT2Data as Data
    from hadou_scheme.hadou_qtt2 import HadouQTT2Scheme as Scheme
elif type == 'sparse3D':
    from data.sparse_data import SparseData as Data
    from hadou_scheme.hadou_sparse import HadouSparseScheme as Scheme
elif type == 'sparse1D':
    from data.sparse1D_data import Sparse1DData as Data
    dim = 1
    initial_pos = initial_pos_kukei1D
    from hadou_scheme.hadou_sparse_1D import HadouSparse1DScheme as Scheme

elif type == 'sparse2D':
    from data.sparse_data import SparseData as Data
    from hadou_scheme.hadou_sparse import HadouSparseScheme as Scheme
    dim = 2
    initial_pos = initial_pos2D
elif type == 'sparse2D-cn':
    from data.sparse_data_cn import SparseDataCN as Data
    from hadou_scheme.hadou_sparse_cn import HadouSparseSchemeCN as Scheme
    dim = 2
    initial_pos = initial_pos2D_yama
elif type == 'sparse2D2':
    from data.sparse2D_data2 import Sparse2DData2 as Data
    initial_pos = initial_pos2D
    dim = 2
else:
    assert(False)

# 1.0/np.sqrt(3)/2.0 = 0.28867513459481292
setting = Setting(n=n, dim=dim, tau=1e-3, tol=1e-4, max_T=1.2, rmax=10000, result_dir='{}/{}'.format(type, file_name))

data = Data(setting, initial_pos)

print("n:{}".format(setting.n))
class Calcurator(Data, Scheme):
    def __init__(self, setting, initial_pos):
        super(Calcurator, self).__init__(setting, initial_pos)
        self.initial_step()


calc = Calcurator(setting, initial_pos)

with Clock(output_path=setting.result_path()) as clock:
    for i in range(setting.max_iter):
        calc.next_step()
        if i%(setting.max_iter/8) == 0 and write:
            calc.write()

        if inspect and i%10 == 0:
            calc.info()

        if i%100 == 0:
            print(i)
            if write:
                calc.show()

if inspect:
    calc.info_write()
else:
    calc.write()
print("{}".format(setting.result_path()))

