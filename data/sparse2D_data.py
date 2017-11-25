import numpy as np
import os
import itertools
import scipy.sparse as sparse
from scipy.sparse import kron
from scipy import matmul

class Sparse2DData:
    def __init__(self, setting, initial_pos):
        self.setting = setting

        N = setting.N

        data = [-2,1] + [1, -2, 1]*(N-2) + [1, -2]

        row = [0,0] + reduce(lambda sum, i: sum + [i, i, i], range(1, N-1), []) + [N-1,N-1]
        col = [0,1] + reduce(lambda sum, i: sum + [i, i+1, i+2], range(0, N-2), []) + [N-2,N-1]

        _L = sparse.csr_matrix((data,(row,col)), (N, N))
        _I = sparse.identity(N)

        self.L = kron(_L, _I) + kron(_I, _L)
        self.L /= setting.h**2

        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = map(initial_pos, itertools.product(space_list, repeat=setting.dim))

        self.q = np.array(q_init_list)
        self.p = setting.tau*self.L.dot(self.q)
        self.step = 0
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

    def energy_calc(self):
        print("{}".format(self.step))
        return
