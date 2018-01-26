import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import os

ns = [6, 7, 8]
# ns = [6,7,8]
class Plot(object):
      def __init__(self, dir_names):
            self.errors = []

            for dir_name in dir_names:
                exact_f = np.loadtxt(os.path.join(dir_name, "info_exact_f.csv"))
                appro_f = np.loadtxt(os.path.join(dir_name, "info_appro_f.csv"))
                self.errors.append(norm(appro_f-exact_f)/norm(exact_f))
                print(dir_name)

      def plot(self):
            plt.plot(ns, self.errors, 'o-')

            # plt.annotate('label_name',
            #       xy=(6, eranks[0]), xycoords='data',
            #       xytext=(-50, 30),
            #       textcoords='offset points',
            #       arrowprops=dict(arrowstyle="->")
            #       )

plt.xlabel("n")
plt.xlim([5.5, 8.5])
plt.xticks(ns, ns)

plt.ylabel("relative error")
plt.ylim([1e-3, 1e-0])
plt.yscale("log")

# plt.ylim([1,20])


plot = Plot(
  [
  'result/sine/qtt3D-cn-deim/sine_2_n_6_tol4_inspect',
  'result/sine/qtt3D-cn-deim/sine_2_n_7_tol4_inspect',
  'result/sine/qtt3D-cn-deim/sine_2_n_8_tol4_inspect'
  # 'result/sine/qtt3D-cn-deim/sine_2_n_8_tol4_inspect',
  # 'result/sine/sparse3D-cn/sine_2_n_8_tol4_nowrite',
  ])


plot.plot()
plt.show()

