import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import os

ns = [6, 7, 8]
# ns = [6,7,8]
class ErrorPlot(object):
      def __init__(self, fulls, label_name, dir_names):

            self.errors = []
            self.label_name = label_name

            for full, dir_name in zip(fulls, dir_names):
              q0 = np.loadtxt(os.path.join(dir_name, "q_0.csv"))
              self.errors.append(norm(q0-full)/norm(full))
              print(dir_name)

      def plot(self):
            plt.plot(ns, self.errors, 'o-', label=self.label_name)

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
plt.ylim([1e-5, 1e-1])
plt.yscale("log")

# plt.ylim([1,20])

fulls = [
np.loadtxt(os.path.join('result/sine/sparse3D-cn/sine_2_n_6_tol8_nowrite', "q_0.csv")),
np.loadtxt(os.path.join('result/sine/sparse3D-cn/sine_2_n_7_tol8_nowrite', "q_0.csv")),
np.loadtxt(os.path.join('result/sine/sparse3D-cn/sine_2_n_8_tol8_nowrite', "q_0.csv")),

]


cg_plot = ErrorPlot(fulls, 'CG-tol:1e-4',
  [
  'result/sine/sparse3D-cn/sine_2_n_6_tol4_nowrite',
  'result/sine/sparse3D-cn/sine_2_n_7_tol4_nowrite',
  'result/sine/sparse3D-cn/sine_2_n_8_tol4_nowrite',
  ])

cg_plot.plot()

# ErrorPlot(fulls, 'QTT-tol:1e-6',
#   [
#   'result/sine/qtt3D-cn/n_6_tol6_nowrite',
#   'result/sine/qtt3D-cn/n_7_tol6_nowrite',
#   # 'result/qtt3D/n_8_tol4',
  # ])
# ErrorPlot(fulls, 'QTT-DEIM-tol:1e-6',
#   [
#   'result/sine/qtt3D-cn-deim/n_6_tol6_nowrite',
#   'result/sine/qtt3D-cn-deim/n_7_tol6_nowrite',
#   # 'result/qtt3D/n_8',
#   ])


qtt_plot = ErrorPlot(fulls, 'QTT-tol:1e-4',
  [
  'result/sine/qtt3D-cn/sine_2_n_6_tol4_nowrite',
  'result/sine/qtt3D-cn/sine_2_n_7_tol4_nowrite',
  'result/sine/qtt3D-cn/sine_2_n_8_tol4_nowrite',
  ])

qtt_plot.plot()

qtt_deim_plot = ErrorPlot(fulls, 'QTT-DEIM-tol:1e-4',
  [
  'result/sine/qtt3D-cn-deim/sine_2_n_6_tol4_nowrite',
  'result/sine/qtt3D-cn-deim/sine_2_n_7_tol4_nowrite',
  'result/sine/qtt3D-cn-deim/sine_2_n_8_tol4_nowrite',
  ])

qtt_deim_plot.plot()


plt.legend(loc="lower right")

plt.show()
