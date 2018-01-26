import itertools
import numpy as np
from numpy.linalg import norm
import os


class SineSparseScheme(object):
    def initial_step(self):
        N = self.setting.N
        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = map(self.initial_pos, itertools.product(space_list, repeat=self.setting.dim))

        self.q = np.array(q_init_list)
        self.p = self.setting.tau*self.L.dot(self.q) - self.setting.tau*np.sin(self.q)
        self.step = 1
        self.write_num = 0

        self.info_E = []

    def next_step(self):
        tau = self.setting.tau
        next_q = self.q + tau*self.p
        next_p = self.p + tau*self.L.dot(next_q) - tau*np.sin(next_q)
        # next_q = next_q + tau/2.0*next_p

        self.q = next_q
        self.p = next_p
        self.step += 1

    def info(self):
        N = self.setting.N
        q = self.q.reshape([N, N, N], order='F')
        p = self.p.reshape([N, N, N], order='F')

        K = norm(p)**2/2.0
        U = -3*norm(q)**2 + reduce(
            lambda sum, i: sum + (q[i,:,:]*q[i+1,:,:]).sum() + (q[:,i,:]*q[:,i+1,:]).sum()+ (q[:,:,i]*q[:,:,i+1]).sum()
            , xrange(self.setting.N-1), 0) + np.cos(q).sum()

        E = K - U/self.setting.h**2
        print("step: {}, t: {}, E: {}".format(self.step, self.step*self.setting.tau, E))

        self.info_E.append(E)

    def info_write(self):
        file_name = os.path.join(self.setting.result_path(), 'info_E.csv')
        np.savetxt(file_name, np.array(self.info_E), delimiter=',')
