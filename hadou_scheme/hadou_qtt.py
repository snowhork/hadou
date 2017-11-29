import itertools
import numpy as np
import tt

class HadouQTTScheme(object):
    def initial_step(self):
        setting = self.setting
        N = setting.N

        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = np.reshape(map(self.initial_pos, itertools.product(space_list, repeat=setting.dim)), setting.qtt_shape(), order='F')

        self.q = tt.vector(q_init_list, setting.tol)
        self.p = (setting.tau*tt.matvec(self.L, self.q)).round(setting.tol, rmax=setting.rmax)

        self.step = 1
        self.write_num = 0

    def next_step(self):
        tau = self.setting.tau
        tol = self.setting.tol
        rmax = self.setting.rmax

        next_q = self.q + tau*self.p
        next_q = next_q.round(tol, rmax=rmax)

        next_p = self.p + tau*tt.matvec(self.L, next_q)
        next_p = next_p.round(tol, rmax=rmax)    

        self.q = next_q
        self.p = next_p
        self.step += 1

