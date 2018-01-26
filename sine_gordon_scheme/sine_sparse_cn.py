import itertools
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import cg
from numpy.linalg import norm
import os

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

        self.info_E = []

    def next_step(self):
        n = self.setting.n
        dim = self.setting.dim
        tau = self.setting.tau

        v = self.B.dot(self.u) - self.old_u - 1*tau*tau*np.sin(self.u)

        self.old_u = self.u
        self.u, _ = cg(self.A, v, x0=v, tol=self.setting.tol)
        self.step += 1

    def info(self):
        N = self.setting.N
        q = self.u.reshape([N, N, N], order='F')
        p = self.u.reshape([N, N, N], order='F') - self.old_u.reshape([N, N, N], order='F')
        p /= self.setting.tau

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
