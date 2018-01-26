
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
plt.ylim([0.998,1.017])


HamiltonianPlot('QTT-tol:1e-4',      'result/sine/qtt3D-cn/sine_2_n_6_tol4_inspect')
HamiltonianPlot('QTT-deim-tol:1e-4', 'result/sine/qtt3D-cn-deim/sine_2_n_6_tol4_inspect_type2_3')
HamiltonianPlot('CG-tol:1e-4',       'result/sine/sparse3D-cn/sine_2_n_6_tol4_inspect')
HamiltonianPlot('CG-tol:1e-8',       'result/sine/sparse3D-cn/sine_2_n_6_tol8_inspect')

# HamiltonianPlot('QTT-tol:1e-4',      'result/sine/qtt3D-cn/sine_2_n_8_tol4_inspect')
# HamiltonianPlot('QTT-deim-tol:1e-4', 'result/sine/qtt3D-cn-deim/sine_2_n_8_tol4_inspect_type2')
# HamiltonianPlot('CG-tol:1e-4',       'result/sine/sparse3D-cn/sine_2_n_8_tol4_inspect')
# HamiltonianPlot('CG-tol:1e-8',       'result/sine/sparse3D-cn/sine_2_n_8_tol8_inspect')

plt.legend(loc="lower right")

plt.show()
