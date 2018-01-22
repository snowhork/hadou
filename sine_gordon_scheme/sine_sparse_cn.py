import itertools
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import cg

class SineSparseCNScheme(object):
    def initial_step(self):
        N = self.setting.N
        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = map(self.initial_pos, itertools.product(space_list, repeat=self.setting.dim))

        self.u = np.array(q_init_list)
        self.old_u = np.array(q_init_list)

        n = self.setting.n
        dim = self.setting.dim
        tau = self.setting.tau

        I = sparse.identity(N**self.setting.dim)

        self.A = I - tau*tau/2*self.L
        self.B = 2*I + tau*tau/2*self.L

        self.step = 0
        self.write_num = 0

    def next_step(self):
        n = self.setting.n
        dim = self.setting.dim
        tau = self.setting.tau

        v = self.B.dot(self.u) - self.old_u + 1*tau*tau*np.sin(self.u)

        self.old_u = self.u
        self.u, _ = cg(self.A, v, x0=v, tol=self.setting.tol)
        self.step += 1
