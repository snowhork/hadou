
import numpy as np
import matplotlib.pyplot as plt
import os

ns = np.arange(120)*10

class HamiltonianPlot(object):
      def __init__(self, label_name, dir_name):
            eranks = np.loadtxt(os.path.join(dir_name, "info_E.csv"))
            plt.plot(ns, eranks/eranks[0], '-', label=label_name)

            # plt.annotate('label_name',
            #       xy=(6, eranks[0]), xycoords='data',
            #       xytext=(-50, 30),
            #       textcoords='offset points',
            #       arrowprops=dict(arrowstyle="->")
            #       )




plt.xlabel("step")
plt.xlim([0, 1200])
# plt.xticks(ns, ns)

plt.ylabel("Hamiltonian")
# plt.ylim([1,20])


HamiltonianPlot('QTT-tol:1e-4', 'result/qtt3D/n_8_tol4_inspect')
HamiltonianPlot('QTT-tol:1e-6', 'result/qtt3D/n_8_inspect')
HamiltonianPlot('Full', 'result/sparse3D/n_8_inspect')

plt.legend(loc="upper right")

plt.show()
