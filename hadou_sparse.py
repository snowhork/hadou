import numpy as np
import itertools
import time
import scipy.sparse as sparse
from scipy.sparse import kron
from scipy import matmul

from setting import Setting

def initial_pos(r):
    return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)*np.sin(r[2]*2*np.pi)

class Data:
    def __init__(self, setting):
        self.setting = setting

        N = setting.N

        data = [-2,1] + [1, -2, 1]*(N-2) + [1, -2]

        row = [0,0] + reduce(lambda sum, i: sum + [i, i, i], range(1, N-1), []) + [N-1,N-1]
        col = [0,1] + reduce(lambda sum, i: sum + [i, i+1, i+2], range(0, N-2), []) + [N-2,N-1]

        _L = sparse.csr_matrix((data,(row,col)), (N, N))
        _I = sparse.identity(N)

        self.L = kron(kron(_L, _I), _I) + kron(kron(_I, _L), _I) + kron(kron(_I, _I), _L)
        self.L /= setting.h**2

        space_list = np.linspace(0, 1, 2**setting.n)
        q_init_list = map(initial_pos, itertools.product(space_list, repeat=setting.dim))

        self.q = np.array(q_init_list)
        self.p = setting.tau*self.L.dot(self.q)
        self.step = 0
        self.write_num = 0

    def next_step(self):
        tau = setting.tau
        next_q = self.q + tau*self.p
        next_p = self.p + tau*self.L.dot(next_q)

        self.q = next_q
        self.p = next_p
        self.step += 1

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'result_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.q, delimiter=',')
        self.write_num += 1

    def energy_calc(self):
        print("{}".format(data.step))
        return
        K = self.p.norm()**2/2.0
        q_full = self.q.full().flatten(order='F')
        U = -self.q.norm()**2 + reduce(lambda sum, i: sum + q_full[i]*q_full[i+1], xrange(setting.N-1), 0)
        U /= self.setting.h**2
        energy = K - U

        print("{}: {}".format(data.step, energy))


current_time = time.strftime("20%y%d%m_%T")

setting = Setting(n=6, dim=3, tau=1e-4, tol=1e-4, max_T=0.5, result_dir='3D/sparse/{}'.format(current_time))

data = Data(setting)

for i in range(setting.max_iter):
    data.next_step()
    if i%(setting.max_iter/9) == 0:
        data.write()

    if i%100 == 0:
        data.energy_calc()
