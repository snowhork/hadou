import numpy as np
import os
import itertools
import scipy.sparse as sparse
from scipy.sparse import kron
from scipy import matmul

class Sparse2DData2:
    def __init__(self, setting, initial_pos):
        self.setting = setting

        N = setting.N

        space_list = np.linspace(0, 1, 2**setting.n+1)
        q_init_list = [[initial_pos((x, y)) for x in space_list] for y in space_list]

        self.old_q = np.array(q_init_list)
        self.q = np.zeros((N+1,N+1))
        for i in range(1, N):
            for j in range(1, N):
                self.q[i, j] = self.old_q[i, j] + 0.5*(setting.tau**2)/(setting.h**2)*(
                    self.old_q[i+1, j] + self.old_q[i, j+1] +
                    self.old_q[i-1, j] + self.old_q[i, j-1] - 4 * self.old_q[i, j]
                    )

        self.step = 0
        self.write_num = 0

    def next_step(self):
        tau = self.setting.tau
        h   = self.setting.h
        N = self.setting.N


        next_q = np.zeros((N+1,N+1))
        for i in range(1, N):
            for j in range(1, N):
                next_q[i, j] = 2*self.q[i, j] - self.old_q[i, j] + (tau**2)/(h**2)*(
                    self.q[i+1, j] + self.q[i, j+1] +
                    self.q[i-1, j] + self.q[i, j-1] - 4 * self.q[i, j]
                    )


        self.old_q = self.q
        self.q = next_q
        self.step += 1

    def write(self):
        file_name = os.path.join(self.setting.result_path(), 'q_{}.csv'.format(self.write_num))
        np.savetxt(file_name, self.q.flatten(order='F'), delimiter=',')

        self.write_num += 1

    def energy_calc(self):
        print("{}".format(self.step))
        return
