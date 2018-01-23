import numpy as np
import itertools
import tt
import os
from numpy.linalg import norm


class QTTData:
    def __init__(self, setting, initial_pos, nuemann=False):
        self.setting = setting
        self.initial_pos = initial_pos
        self.L = (-1.0/(setting.h*setting.h))*tt.qlaplace_dd([setting.n]*setting.dim)

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'q_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.q.full().flatten(order='F'), delimiter=',')

        file_name = os.path.join(self.setting.result_path(), 'p_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.p.full().flatten(order='F'), delimiter=',')
        self.write_num += 1

        print("write: step: {}, t: {}".format(self.step, self.step*self.setting.tau))

    def show(self):
        N = self.setting.N
        q = self.q.full().flatten(order='F').reshape([N, N, N], order='F')
        p = self.p.full().flatten(order='F').reshape([N, N, N], order='F')

        K = norm(p)**2/2.0
        U = -3*norm(q)**2 + reduce(
            lambda sum, i: sum + (q[i,:,:]*q[i+1,:,:]).sum() + (q[:,i,:]*q[:,i+1,:]).sum()+ (q[:,:,i]*q[:,:,i+1]).sum()
            , xrange(self.setting.N-1), 0)

        E = K - U/self.setting.h**2
        print("step: {}, t: {}, r: {} E: {}".format(self.step, self.step*self.setting.tau, self.q.erank, E))
