import itertools
import numpy as np
import tt
import os
import util
from tt.amen import amen_solve
from numpy.linalg import norm

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

        self.info_E = []
        self.info_erank = []


    def next_step(self):
        tau = self.setting.tau
        tol = self.setting.tol

        sine= tt.vector(1*tau*tau*np.sin(self.q.full()), tol)

        v = tt.matvec(self.B, self.q) - self.old_q - sine

        self.old_q = self.q
        self.q = amen_solve(self.A, v, v, tol, verb=0)
        self.step += 1

    def info(self):
        N = self.setting.N
        q = self.q.full().flatten(order='F').reshape([N, N, N], order='F')
        old_q = self.old_q.full().flatten(order='F').reshape([N, N, N], order='F')
        p = (q - old_q)/self.setting.tau

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



