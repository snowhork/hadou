import numpy as np
from scipy.linalg import toeplitz
import itertools
import tt

def initial_pos(r):
    return np.sin(2*np.pi*r)

class Setting:
    def __init__(self, n, dim, tau, tol):
        self.n = n
        self.dim = dim
        self.tau = tau
        self.tol = tol
        self.h = 1.0/(2**n+1)


class Data:
    def __init__(self, setting):
        self.setting = setting
        self.L = toeplitz([-2, 1] + [0]*(2**setting.n-2))/(setting.h**2)

        space_list = np.linspace(0, 1, 2**setting.n)
        q_init_list = initial_pos(space_list)

        self.q = q_init_list
        self.p = np.zeros(2**setting.n)
        self.step = 0
        self.write_num = 0

    def next_step(self):
        tau = setting.tau
        next_q = self.q + tau*self.p
        next_p = self.p + tau*np.matmul(self.L, next_q)

        self.q = next_q
        self.p = next_p
        self.step += 1

    def write(self):
        np.savetxt('result/test4/test4_{}.csv'.format(self.write_num), self.q, delimiter=',')
        self.write_num += 1


setting = Setting(n=10, dim=1, tau=1e-4, tol=1e-10)

data = Data(setting)

for i in range(5000):
    print(i)
    data.next_step()
    if i%500 == 0:
        data.write()
