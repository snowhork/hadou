import numpy as np
from numpy.linalg import norm
import os
import itertools
import scipy.sparse as sparse
from scipy.sparse import kron
from scipy import matmul

class Sparse1DData:
    def __init__(self, setting, initial_pos):
        self.setting = setting
        self.initial_pos = initial_pos

        N = setting.N

        data = [-2.,1.] + [1., -2., 1.]*(N-2) + [1., -2.]

        row = [0,0] + reduce(lambda sum, i: sum + [i, i, i], range(1, N-1), []) + [N-1,N-1]
        col = [0,1] + reduce(lambda sum, i: sum + [i, i+1, i+2], range(0, N-2), []) + [N-2,N-1]

        self.L = sparse.csr_matrix((data,(row,col)), (N, N))
        self.L /= setting.h**2

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'q_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.q, delimiter=',')

        file_name = os.path.join(self.setting.result_path(), 'p_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.p, delimiter=',')
        self.write_num += 1

    def show(self):
        K = norm(self.p)**2/2.0
        U = -norm(self.q)**2 + reduce(lambda sum, i: sum + self.q[i]*self.q[i+1], xrange(self.setting.N-1), 0)
        U /= self.setting.h**2
        energy = K - U

        print("step: {}, t: {}, E: {}".format(self.step, self.step*self.setting.tau, energy))

