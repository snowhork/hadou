import numpy as np
import matplotlib.pyplot as plt
import itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

t_list = np.linspace(0, 0.25, 10)[:-1]

def exact(r, t):
    return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)*np.sin(r[2]*2*np.pi)*np.cos(2*np.pi*t)

n = 6
N = 2**n

space_list = np.linspace(0, 1, N)
X, Y = np.meshgrid(space_list, space_list)

fig = plt.figure()

for i, t in enumerate(t_list):

    q_exact = np.array(map(lambda r: exact(r, t), itertools.product(space_list, repeat=3)))
    q = q_exact.reshape([N, N, N], order='F')

    Z = q[20, :, :]

    fig.suptitle('t={}'.format(t))        
    ax = fig.add_subplot(3, 3, i+1, projection='3d')
    ax.set_zlim([-1, 1])
    surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm, cstride=4, rstride=4, antialiased=True)

plt.show()
