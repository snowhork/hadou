# encoding: utf-8

import numpy as np
import sys, os, yaml
import matplotlib.pyplot as plt
import itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

base_path = sys.argv[1]
base_name = 'q'

with open(os.path.join(base_path, 'setting.yml'), "r") as f:
    setting = yaml.load(f)

# t_list = [0, 2, 4, 6]
t_list = range(9)
n = setting['n']
dim = setting['dim']
N = 2**n

space_list = np.linspace(0, 1, N+2)[1:N+1]
X, Y = np.meshgrid(space_list, space_list)

fig = plt.figure()

if dim == 1:
    for i, t in enumerate(t_list):
        q = np.loadtxt(os.path.join(base_path, "{}_{}.csv".format(base_name, t)))

        ax = fig.add_subplot(3, 3, i+1)
        ax.set_ylim([-1, 1])

        surf = ax.plot(space_list,q)

else:
    for i, t in enumerate(t_list):

        q = np.loadtxt(os.path.join(base_path, "{}_{}.csv".format(base_name, t)))

        # fig.suptitle('t={}'.format(t))

        num = 3
        if len(t_list) == 4:
            num = 2
        ax = fig.add_subplot(num, num, i+1, projection='3d')

        if dim == 3:
            q = q.reshape([N, N, N], order='F')
            Z = q[32, :, :]
            max_iter = int(setting['max_T']/setting['tau'])
            _t = max_iter/8*t*setting['tau']
            ax.set_title("t={}".format(_t))
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("u(x,y,z)")


        elif dim == 2:
            Z = q.reshape([N, N], order='F')

        # ax.set_zlim([-0.5, 0.5])
        # n=7: n-2 n=8: n
        surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm, cstride=n, rstride=n, antialiased=True)

plt.show()
