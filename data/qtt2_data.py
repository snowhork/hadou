import numpy as np
import itertools
import tt
import os

class QTT2Data:
    def __init__(self, setting, initial_pos):
        self.setting = setting
        self.initial_pos = initial_pos

        tau = setting.tau

        L = (-1.0/(setting.h*setting.h))*tt.qlaplace_dd([setting.n]*setting.dim)

        I_tt = tt.diag(tt.vector(np.ones(setting.N**setting.dim).reshape([2]*setting.n*setting.dim)))

        I1 = tt.matrix(np.array([[1,0],[0,0]]))
        I2 = tt.matrix(np.array([[0,1],[0,0]]))
        I3 = tt.matrix(np.array([[0,0],[1,0]]))
        I4 = tt.matrix(np.array([[0,0],[0,1]]))
        A1 = tt.kron(I_tt, I1)
        A2 = tau*tt.kron(I_tt, I2)
        A3 = tau*tt.kron(L, I3)
        A4 = tt.kron(I_tt, I4) + tau*tau*tt.kron(L, I4)

        self.A = (A1 + A2 + A3 + A4).round(setting.tol)

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'x_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.x.full().flatten(order='F'), delimiter=',')

        self.write_num += 1

        print("write: step: {}, t: {}".format(self.step, self.step*self.setting.tau))
        
    def show(self):
        print("step: {}, t: {}, r: {}".format(self.step, self.step*self.setting.tau, self.x.erank))
