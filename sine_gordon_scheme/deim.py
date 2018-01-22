import numpy as np
from numpy import matmul
from scipy.linalg import solve

def DEIM(U, N, M):
    P = np.zeros((M, N))
    B = np.zeros(M, dtype=int)

    u = U[:, 0]
    B[0] = np.argmax(abs(u))
    P[0, B[0]] = 1

    for l in range(1, M):
        u = U[:, l]
        c = solve(matmul(P[:l, :], U[:, :l]), matmul(P[:l, :], u))
        r = u - matmul(U[:, :l], c)

        B[l] = np.argmax(abs(u))
        P[l, B[l]] = 1

    return P, B
