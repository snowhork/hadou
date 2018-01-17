import itertools
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve

class HadouSparseSchemeCN(object):
    def initial_step(self):
        N = self.setting.N
        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = map(self.initial_pos, itertools.product(space_list, repeat=self.setting.dim))

        self.u = np.array(q_init_list)
        self.old_u = np.array(q_init_list)

        self.step = 0
        self.write_num = 0

    def next_step(self):
        N = self.setting.N
        tau = self.setting.tau
        I = sparse.identity(N**self.setting.dim)

        A = I - tau*tau/2*self.L
        B = 2*I + tau*tau/2*self.L

        v = B.dot(self.u) - self.old_u

        self.old_u = self.u
        self.u = spsolve(A, v)
        self.step += 1
