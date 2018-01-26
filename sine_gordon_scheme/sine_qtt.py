import itertools
import numpy as np
import tt, os
from numpy.linalg import norm

class SineQTTScheme(object):
    def initial_step(self):
        setting = self.setting
        N = setting.N

        space_list = np.linspace(0, 1, N+2)[1:N+1]
        q_init_list = np.reshape(map(self.initial_pos, itertools.product(space_list, repeat=setting.dim)), setting.qtt_shape(), order='F')

        self.q = tt.vector(q_init_list, setting.tol)
        self.p = setting.tau*(tt.matvec(self.L, self.q) - tt.vector(np.sin(q_init_list), setting.tol))
        self.p = self.p.round(setting.tol, rmax=setting.rmax)

        self.step = 1
        self.write_num = 0

        self.info_E = []
        self.info_erank = []

    def next_step(self):
        tau = self.setting.tau
        tol = self.setting.tol
        rmax = self.setting.rmax

        next_q = self.q + tau*self.p
        next_q = next_q.round(tol, rmax=rmax)

        next_p = self.p + tau*(tt.matvec(self.L, next_q) - tt.vector(np.sin(next_q.full()), tol))
        next_p = next_p.round(tol, rmax=rmax)

        self.q = next_q
        self.p = next_p
        self.step += 1

    def info(self):
        N = self.setting.N
        q = self.q.full().flatten(order='F').reshape([N, N, N], order='F')
        p = self.p.full().flatten(order='F').reshape([N, N, N], order='F')

        K = norm(p)**2/2.0
        U = -3*norm(q)**2 + reduce(
            lambda sum, i: sum + (q[i,:,:]*q[i+1,:,:]).sum() + (q[:,i,:]*q[:,i+1,:]).sum()+ (q[:,:,i]*q[:,:,i+1]).sum()
            , xrange(self.setting.N-1), 0) + np.cos(q).sum()

        E = K - U/self.setting.h**2
        print("step: {}, t: {}, r: {} E: {}".format(self.step, self.step*self.setting.tau, self.q.erank, E))

        self.info_E.append(E)
        self.info_erank.append(self.q.erank)

    def info_write(self):
        file_name = os.path.join(self.setting.result_path(), 'info_E.csv')
        np.savetxt(file_name, np.array(self.info_E), delimiter=',')

        file_name = os.path.join(self.setting.result_path(), 'info_erank.csv')
        np.savetxt(file_name, np.array(self.info_erank), delimiter=',')



