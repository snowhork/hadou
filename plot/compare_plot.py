import numpy as np
import sys, os, yaml
import matplotlib.pyplot as plt
import itertools

qtt_path = sys.argv[1]
full_model_path = sys.argv[2]


n = 6
dim = 3
N = 2**n

qtt_q = np.loadtxt(qtt_path)
full_q = np.loadtxt(full_model_path)

space_list = np.linspace(0, 1, N+2)[1:N+1]

y_i = 32
z_i = 32

plt.plot(space_list, qtt_q.reshape([N, N, N], order='F')[z_i, y_i, :], label="qtt_format")
plt.plot(space_list, full_q.reshape([N, N, N], order='F')[z_i, y_i, :], label="full_model")
plt.legend(loc="lower right")
plt.xlabel("x")
plt.ylabel("u(x,y,z)")

plt.show()
