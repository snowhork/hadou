import itertools
import numpy as np
import tt
from tt.amen import amen_mv

class HadouQTT2Scheme(object):
    def initial_step(self):
        setting = self.setting
        N = setting.N

        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = map(self.initial_pos, itertools.product(space_list, repeat=setting.dim))
        p_init_list = np.zeros(N**setting.dim)

        init_x = np.concatenate((q_init_list, p_init_list)).reshape([2] + setting.qtt_shape(), order='F')

        self.x = tt.vector(init_x, setting.tol)
        self.step = 0
        self.write_num = 0

    def next_step(self):
        tau = self.setting.tau
        tol = self.setting.tol
        rmax = self.setting.rmax

        next_x, _ = amen_mv(self.A, self.x, tol, verb=False)

        self.x = next_x
        self.step += 1

