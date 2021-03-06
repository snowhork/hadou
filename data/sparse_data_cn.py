import numpy as np
import os
import itertools
import scipy.sparse as sparse
from scipy.sparse import kron
from scipy import matmul

class SparseDataCN(object):
    def __init__(self, setting, initial_pos, neumann=False):
        self.setting = setting
        self.initial_pos = initial_pos
        initial_pos = self.initial_pos
        setting = self.setting

        N = setting.N

        if neumann:
            data = [-1, 1] + [1, -2, 1]*(N-2) + [1, -1]
        else:
            data = [-2, 1] + [1, -2, 1]*(N-2) + [1, -2]

        row = [0,0] + reduce(lambda sum, i: sum + [i, i, i], range(1, N-1), []) + [N-1,N-1]
        col = [0,1] + reduce(lambda sum, i: sum + [i, i+1, i+2], range(0, N-2), []) + [N-2,N-1]

        _L = sparse.csr_matrix((data,(row,col)), (N, N))
        _I = sparse.identity(N)

        assert(setting.dim == 2 or setting.dim == 3)
        if setting.dim == 3:
            self.L = kron(kron(_L, _I), _I) + kron(kron(_I, _L), _I) + kron(kron(_I, _I), _L)
        elif setting.dim == 2:
            self.L = kron(_L, _I) + kron(_I, _L)

        self.L /= setting.h**2

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'q_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.u, delimiter=',')

        self.write_num += 1

        print("write: step: {}, t: {}".format(self.step, self.step*self.setting.tau))

    def show(self):
        print("step: {}, t: {}".format(self.step, self.step*self.setting.tau))
