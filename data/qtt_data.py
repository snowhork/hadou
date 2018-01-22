import numpy as np
import itertools
import tt
import os

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
        print("step: {}, t: {}, r: {}".format(self.step, self.step*self.setting.tau, self.q.erank))
