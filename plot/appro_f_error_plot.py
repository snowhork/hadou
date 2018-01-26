import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import os

ns = np.arange(50, 1200)
# ns = [6,7,8]
class Plot(object):
      def __init__(self, label, dir_name):
            self.error = np.loadtxt(os.path.join(dir_name, "info_appro_f_error.csv"))
            self.label = label
            print(dir_name)

      def plot(self):
            plt.plot(ns, self.error, '-', label=self.label)

            # plt.annotate('label_name',
            #       xy=(6, eranks[0]), xycoords='data',
            #       xytext=(-50, 30),
            #       textcoords='offset points',
            #       arrowprops=dict(arrowstyle="->")
            #       )

plt.xlabel("step")
plt.xlim([50, 1200])
# plt.xticks(ns, ns)

plt.ylabel("relative error")
# plt.ylim([1e-3, 1e-0])
# plt.yscale("log")

# plt.ylim([1,20])


plot6 = Plot("n=6", "result/sine/qtt3D-cn-deim/sine_2_n_6_tol4_inspect_type2_3")
plot7 = Plot("n=7", "result/sine/qtt3D-cn-deim/sine_2_n_7_tol4_inspect_type2_22")
plot8 = Plot("n=8", "result/sine/qtt3D-cn-deim/sine_2_n_8_tol4_inspect_type2")
plot6.plot()
plot7.plot()
plot8.plot()


plt.legend(loc="upper right")

plt.show()

