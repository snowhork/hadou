import itertools
import numpy as np

class SineSparseScheme(object):
    def initial_step(self):
        N = self.setting.N
        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = map(self.initial_pos, itertools.product(space_list, repeat=self.setting.dim))

        self.q = np.array(q_init_list)
        self.p = self.setting.tau*self.L.dot(self.q) + np.sin(self.q)
        self.step = 1
        self.write_num = 0

    def next_step(self):
        tau = self.setting.tau
        next_q = self.q + tau/2.0*self.p
        next_p = self.p + tau*self.L.dot(next_q) + np.sin(next_q)
        next_q = next_q + tau/2.0*next_p

        self.q = next_q
        self.p = next_p
        self.step += 1  

