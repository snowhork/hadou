import itertools
import numpy as np
import tt
from scipy.linalg import inv
from scipy.linalg.interpolative import svd
from tt.amen import amen_solve
from numpy import matmul
from scipy.linalg import inv

from deim import DEIM
import util
from numpy.linalg import norm
import os

class SineQTTCNSchemeDEIM2(object):
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

        self.deim_m = 2
        self.deim_M = 2**self.deim_m
        self.n_snapshot = 32
        self.snapshots = np.zeros((self.setting.N**self.setting.dim, self.n_snapshot))
        self.snapshots_count = 0

        self.info_E = []
        self.info_erank = []


    def next_step(self):
        tau = self.setting.tau
        tol = self.setting.tol

        tt_sine = 0
        if self.snapshots_count >= self.n_snapshot:
            if self.snapshots_count == self.n_snapshot:
                with util.Clock("---get appro_f---") as clock:
                    tt_sine = self.get_appro_f(tau).round(tol)
            else:
                tt_sine = self.get_appro_f(tau).round(tol)
            self.snapshots_count+=1
        else:
            if self.snapshots_count == self.n_snapshot-1:
                with util.Clock("---get f---") as clock:
                    sine = 1*tau*tau*np.sin(self.q.full())
            else:
                sine = 1*tau*tau*np.sin(self.q.full())

            self.snapshots[: ,self.snapshots_count] = sine.flatten(order='F')
            self.snapshots_count+=1
            if self.snapshots_count == self.n_snapshot:
                self.construct_deim()
            tt_sine =tt.vector(sine, tol)

        v = tt.matvec(self.B, self.q) - self.old_q + tt_sine

        self.old_q = self.q
        self.q = amen_solve(self.A, v, v, tol, verb=0)
        self.step += 1

    def construct_deim(self):
        self.deim_setting = QTT_DEIM_setting(n=self.setting.n*self.setting.dim, m=self.deim_m, n_snapshot=self.n_snapshot, N=self.setting.N**self.setting.dim, M=self.deim_M)
        self.deim = get_deim(self.deim_setting, self.snapshots)

    def get_appro_f(self, tau):
        appro_f = self.deim.W.dot(get_f_p(self.deim.B, self.q, self.deim_setting.n, tau))

        appro_f_tensor = tt.vector(appro_f.reshape(self.setting.qtt_shape(), order='F'), self.setting.tol)
        return appro_f_tensor

    def info(self):
        N = self.setting.N
        q = self.q.full().flatten(order='F').reshape([N, N, N], order='F')
        old_q = self.old_q.full().flatten(order='F').reshape([N, N, N], order='F')
        p = (q - old_q)/self.setting.tau

        K = norm(p)**2/2.0
        U = -3*norm(q)**2 + reduce(
            lambda sum, i: sum + (q[i,:,:]*q[i+1,:,:]).sum() + (q[:,i,:]*q[:,i+1,:]).sum()+ (q[:,:,i]*q[:,:,i+1]).sum()
            , xrange(self.setting.N-1), 0) - np.cos(q).sum()

        E = K - U/self.setting.h**2
        print("step: {}, t: {}, r: {} E: {}".format(self.step, self.step*self.setting.tau, self.q.erank, E))

        self.info_E.append(E)
        self.info_erank.append(self.q.erank)

    def info_write(self):
        file_name = os.path.join(self.setting.result_path(), 'info_E.csv')
        np.savetxt(file_name, np.array(self.info_E), delimiter=',')

        file_name = os.path.join(self.setting.result_path(), 'info_erank.csv')
        np.savetxt(file_name, np.array(self.info_erank), delimiter=',')

class QTT_DEIM_setting:
    def __init__(self, n, m, n_snapshot, N, M):
        self.n = n
        self.n_snapshot = n_snapshot
        self.m = m

        self.N = N
        self.M = M

class DEIM_result:
    def __init__(self, W, B):
        self.W = W
        self.B = B

def get_f_p(B, x, n, tau):
    return np.array([tau*tau*np.sin(x.__getitem__(util.to_quantized_index(b, n))) for b in B])

def get_deim(setting, snapshots):
    with util.Clock("---DEIM preprocess---") as clock:
        U, _, _ = svd(snapshots, setting.M)
        P, B = DEIM(U, setting.N, setting.M)
        W = matmul(U, inv(matmul(P, U)))
        res = DEIM_result(W, B)

    return res
