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

        if dim == 3:
            q = q.reshape([N, N, N], order='F')
            Z = q[16, :, :]

        elif dim == 2:
            q = q.reshape([N, N], order='F')
            Z = q[16, 16, :]

        fig.suptitle('t={}'.format(t))        
        ax = fig.add_subplot(3, 3, i+1, projection='3d')
        ax.set_zlim([-1, 1])
        surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm, cstride=n-2, rstride=n-2, antialiased=True)

plt.show()
