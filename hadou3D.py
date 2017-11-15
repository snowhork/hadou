import numpy as np
import itertools
import tt
import os

def initial_pos(r):
    return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)*np.sin(r[2]*2*np.pi)

class Setting:
    def __init__(self, n, dim, tau, tol, max_T, result_dir):
        self.n = n
        self.dim = dim
        self.tau = tau
        self.tol = tol
        self.N = 2**n
        self.h = 1.0/(self.N+1)
        self.result_dir = result_dir
        self.max_T = max_T
        if not os.path.exists(self.result_path()):
            os.makedirs(self.result_path())

        print("max_iter: {}".format(self.max_iter))


    def qtt_shape(self):
        return [2]*(setting.n*setting.dim)

    def result_path(self):
        return "result/{}".format(self.result_dir)

    @property
    def max_iter(self):
        return int(self.max_T/self.tau)

class Data:
    def __init__(self, setting):
        self.setting = setting
        self.L = (-1.0/(setting.h*setting.h))*tt.qlaplace_dd([setting.n]*setting.dim)

        space_list = np.linspace(0, 1, 2**setting.n)
        q_init_list = np.reshape(map(initial_pos, itertools.product(space_list, repeat=setting.dim)), setting.qtt_shape(), order='F')

        self.q = tt.vector(q_init_list, setting.tol)
        self.p = (setting.tau*tt.matvec(self.L, self.q)).round(setting.tol)        
        self.step = 0
        self.write_num = 0

    def next_step(self):
        tau = setting.tau
        next_q = self.q + tau*self.p
        next_q = next_q.round(setting.tol)
        next_p = self.p + tt.matvec(tau*self.L, next_q)
        next_p = next_p.round(setting.tol)

        self.q = next_q
        self.p = next_p
        self.step += 1

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'result_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.q.full().flatten(order='F'), delimiter=',')
        self.write_num += 1

    def energy_calc(self):
        print("{}: {}".format(data.step, data.q.erank))
        return
        K = self.p.norm()**2/2.0
        q_full = self.q.full().flatten(order='F')
        U = -self.q.norm()**2 + reduce(lambda sum, i: sum + q_full[i]*q_full[i+1], xrange(setting.N-1), 0)
        U /= self.setting.h**2
        energy = K - U

        print("{}: {}".format(data.step, energy))


setting = Setting(n=6, dim=3, tau=1e-5, tol=1e-10, max_T=0.5, result_dir='3D/qtt_test1')

data = Data(setting)

for i in range(setting.max_iter):
    data.next_step()
    if i%(setting.max_iter/9) == 0:
        data.write()

    if i%100 == 0:
        data.energy_calc()
