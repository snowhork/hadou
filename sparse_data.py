import numpy as np
import os
import itertools
import scipy.sparse as sparse
from scipy.sparse import kron
from scipy import matmul

class SparseData:
    def __init__(self, setting, initial_pos):
        self.setting = setting

        N = setting.N

        data = [-2,1] + [1, -2, 1]*(N-2) + [1, -2]

        row = [0,0] + reduce(lambda sum, i: sum + [i, i, i], range(1, N-1), []) + [N-1,N-1]
        col = [0,1] + reduce(lambda sum, i: sum + [i, i+1, i+2], range(0, N-2), []) + [N-2,N-1]

        _L = sparse.csr_matrix((data,(row,col)), (N, N))
        _I = sparse.identity(N)

        self.L = kron(kron(_L, _I), _I) + kron(kron(_I, _L), _I) + kron(kron(_I, _I), _L)
        self.L /= setting.h**2

        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = map(initial_pos, itertools.product(space_list, repeat=setting.dim))

        self.q = np.array(q_init_list)
        self.p = setting.tau*self.L.dot(self.q)
        self.step = 1
        self.write_num = 0

    def next_step(self):
        tau = self.setting.tau
        next_q = self.q + tau*self.p
        next_p = self.p + tau*self.L.dot(next_q)

        self.q = next_q
        self.p = next_p
        self.step += 1

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'q_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.q, delimiter=',')

        file_name = os.path.join(self.setting.result_path(), 'p_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.p, delimiter=',')
        self.write_num += 1

        print("write: step: {}, t: {}".format(self.step, self.step*self.setting.tau))

    def energy_calc(self):
        print("{}".format(self.step))
        return
        K = self.p.norm()**2/2.0
        q_full = self.q.full().flatten(order='F')
        U = -self.q.norm()**2 + reduce(lambda sum, i: sum + q_full[i]*q_full[i+1], xrange(setting.N-1), 0)
        U /= self.setting.h**2
        energy = K - U

        print("{}: {}".format(data.step, energy))
