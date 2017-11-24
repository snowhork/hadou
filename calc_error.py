import numpy as np
import itertools

def exact(r, t):
    return np.sin(r[0]*2*np.pi)*np.sin(r[1]*2*np.pi)*np.sin(r[2]*2*np.pi)*np.cos(np.sqrt(3)*2*t*np.pi)



N = 2**7

space_list = np.linspace(0, 1, N+2)[1:N+1]


sparse_q = np.loadtxt('result/sparse3D/n_6_tau1e-4/q_9.csv')
qttr10_q = np.loadtxt('result/qtt3D/n_6_r_10/q_9.csv')
qttr20_q = np.loadtxt('result/qtt3D/n_6_r_20/q_9.csv')

q_exact = np.array(map(lambda r: exact(r, 0.5774), itertools.product(space_list, repeat=3)))




np.linalg.norm(q_exact - qttr10_q)

np.linalg.norm(q_exact - qttr20_q)

np.linalg.norm(q_exact - sparse_q)


# n = 6
# qtt_r10: 17.513926785110183
# qtt_r20: 18.166070157844839
# sparse_q: 18.208424152528991

# n = 7
# qtt_r10: 22.615033513464549
# qtt_r20: 24.999887551691323
# sparse_q: 25.378536064323068
