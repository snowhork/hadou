import numpy as np
import os,sys,yaml
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

space_list = np.linspace(0, 1, N+2)[1:N+1]

fig = plt.figure()

for i, t in enumerate(t_list):

    q = np.loadtxt(os.path.join(base_path, "{}_{}.csv".format(base_name, t)))

    ax = fig.add_subplot(3, 3, i+1)
    ax.set_ylim([-1, 1])
    surf = ax.plot(space_list,q)


plt.show()
