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
N = 2**n

space_list = np.linspace(0, 1, N)
X, Y = np.meshgrid(space_list, space_list)

fig = plt.figure()

for i, t in enumerate(t_list):

    q = np.loadtxt(os.path.join(base_path, "{}_{}.csv".format(base_name, t)))
    q = q.reshape([N, N], order='F')

    Z = q

    fig.suptitle('t={}'.format(t))        
    ax = fig.add_subplot(3, 3, i+1, projection='3d')
    ax.set_zlim([-1, 1])
    surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm, cstride=n-2, rstride=n-2, antialiased=True)

plt.show()
