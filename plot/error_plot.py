import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import os

ns = [6, 7, 8]

class ErrorPlot(object):
      def __init__(self, fulls, label_name, dir_names):

            errors = []

            for full, dir_name in zip(fulls, dir_names):
              q0 = np.loadtxt(os.path.join(dir_name, "q_0.csv"))
              errors.append(norm(q0-full)/norm(full))
              print(dir_name)
            plt.plot(ns, errors, 'o-', label=label_name)

            # plt.annotate('label_name',
            #       xy=(6, eranks[0]), xycoords='data',
            #       xytext=(-50, 30),
            #       textcoords='offset points',
            #       arrowprops=dict(arrowstyle="->")
            #       )




plt.xlabel("step")
plt.xlim([5.5, 8.5])
plt.xticks(ns, ns)

plt.ylabel("relative error")
plt.yscale("log")

# plt.ylim([1,20])

fulls = [
np.loadtxt(os.path.join('result/sparse3D/n_6', "q_0.csv")),
np.loadtxt(os.path.join('result/sparse3D/n_7', "q_0.csv")),
np.loadtxt(os.path.join('result/sparse3D/n_8', "q_0.csv"))]

ErrorPlot(fulls, 'QTT-tol:1e-4',
  [
  'result/qtt3D/n_6_tol4',
  'result/qtt3D/n_7_tol4',
  'result/qtt3D/n_8_tol4',
  ])
ErrorPlot(fulls, 'QTT-tol:1e-6',
  [
  'result/qtt3D/n_6',
  'result/qtt3D/n_7',
  'result/qtt3D/n_8',
  ])

plt.legend(loc="upper right")

plt.show()
