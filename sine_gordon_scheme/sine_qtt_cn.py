import itertools
import numpy as np
import tt
import util
from tt.amen import amen_solve

class SineQTTCNScheme(object):
    def initial_step(self):
        setting = self.setting
        N = setting.N
        n = setting.n
        dim = setting.dim
        tau = setting.tau

        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = np.reshape(map(self.initial_pos, itertools.product(space_list, repeat=setting.dim)), setting.qtt_shape(), order='F')

        self.q = tt.vector(q_init_list, setting.tol)
        self.old_q = tt.vector(q_init_list, setting.tol)

        I = tt.eye(2, n*dim)

        self.A = I - tau*tau/2*self.L
        self.A = self.A.round(setting.tol)

        self.B = 2*I + tau*tau/2*self.L
        self.B = self.B.round(setting.tol)

        self.step = 1
        self.write_num = 0

    def next_step(self):
        tau = self.setting.tau
        tol = self.setting.tol

        sine= tt.vector(1*tau*tau*np.sin(self.q.full()), tol)

        v = tt.matvec(self.B, self.q) - self.old_q + sine

        self.old_q = self.q
        self.q = amen_solve(self.A, v, v, tol, verb=0)
        self.step += 1
