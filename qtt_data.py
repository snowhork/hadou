import numpy as np
import itertools
import tt
import os

class QTTData:
    def __init__(self, setting, initial_pos):
        self.setting = setting
        self.L = (-1.0/(setting.h*setting.h))*tt.qlaplace_dd([setting.n]*setting.dim)

        space_list = np.linspace(0, 1, 2**setting.n)
        q_init_list = np.reshape(map(initial_pos, itertools.product(space_list, repeat=setting.dim)), setting.qtt_shape(), order='F')

        self.q = tt.vector(q_init_list, setting.tol)
        self.p = (setting.tau*tt.matvec(self.L, self.q)).round(setting.tol, rmax=setting.rmax)
        self.step = 0
        self.write_num = 0

    def next_step(self):
        tau = self.setting.tau
        tol = self.setting.tol
        rmax = self.setting.rmax

        next_q = self.q + tau*self.p
        next_q = next_q.round(tol, rmax=rmax)
        next_p = self.p + tt.matvec(tau*self.L, next_q)
        next_p = next_p.round(tol, rmax=rmax)

        self.q = next_q
        self.p = next_p
        self.step += 1

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'q_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.q.full().flatten(order='F'), delimiter=',')

        file_name = os.path.join(self.setting.result_path(), 'p_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.p.full().flatten(order='F'), delimiter=',')
        self.write_num += 1

    def energy_calc(self):
        print("{}: {}".format(self.step, self.q.erank))
        return
        K = self.p.norm()**2/2.0
        q_full = self.q.full().flatten(order='F')
        U = -self.q.norm()**2 + reduce(lambda sum, i: sum + q_full[i]*q_full[i+1], xrange(setting.N-1), 0)
        U /= self.setting.h**2
        energy = K - U

        print("{}: {}".format(data.step, energy))
