import numpy as np
import matplotlib.pyplot as plt
import os

ns = np.arange(120)*10

class ErankPlot(object):
      def __init__(self, label_name, dir_name):
            eranks = np.loadtxt(os.path.join(dir_name, "info_erank.csv"))
            plt.plot(ns, eranks, '-', label=label_name)

            # plt.annotate('label_name',
            #       xy=(6, eranks[0]), xycoords='data',
            #       xytext=(-50, 30),
            #       textcoords='offset points',
            #       arrowprops=dict(arrowstyle="->")
            #       )




plt.xlabel("step")
plt.xlim([0, 1200])
# plt.xticks(ns, ns)

plt.ylabel("effective rank")
plt.ylim([1,20])


ErankPlot('n=6', 'result/qtt3D/n_6_tol4_inspect')
ErankPlot('n=7', 'result/qtt3D/n_7_tol4_inspect')
ErankPlot('n=8', 'result/qtt3D/n_8_tol4_inspect')


plt.legend(loc="lower right")

plt.show()
