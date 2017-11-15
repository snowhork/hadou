import numpy as np
import os
import matplotlib.pyplot as plt
import itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

base_path = 'result/test3/'
base_name = 'test3'

t_list = range(9)
n = 10
N = 2**n

space_list = np.linspace(0, 1, N)
X, Y = np.meshgrid(space_list, space_list)


fig = plt.figure()

for i, t in enumerate(t_list):

    q = np.loadtxt(os.path.join(base_path, "{}_{}.csv".format(base_name, t)))
    # q = q.reshape([N, N, N], order='F')

    # Z = q[20, :, :]

#    fig.suptitle('t={}'.format(t))        
    # fig.subplot(3, 3, i+1)
    # ax = fig.add_subplot(3, 3, i+1, projection='3d')
    # surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm, cstride=3, rstride=3, antialiased=False)
    ax = fig.add_subplot(3, 3, i+1)
    ax.set_ylim([-1, 1])
    surf = ax.plot(space_list,q)


plt.show()
