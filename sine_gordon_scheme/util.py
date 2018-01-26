import numpy as np
import tt
import time

def to_quantized_index(index, n): # fortran index order
    res = []
    for i in format(index,'b').zfill(n)[::-1]:
        res.append(int(i))

    return res

def to_qtt_matrix(A, n, m, eps=1e-14, rmax=100000):
    res = tt.matrix()

    d = n
    res.n = np.array([2]*n)
    res.m = np.array([2]*m + [1]*(n-m))
    prm = np.arange(2 * d)
    prm = prm.reshape((d, 2), order='F')
    prm = prm.T
    prm = prm.flatten('F')
    prm = filter(lambda x: x < n + m, prm)
    sz = res.n * res.m
    b = A.reshape([2]*n + [2]*m, order='F').transpose(prm).reshape(sz, order='F')
    res.tt = tt.vector(b, eps, rmax)
    return res

def to_qtt_matvector(v, n, m, eps=1e-14, rmax=100000):
    res = tt.matrix()

    d = n
    res.n = np.array([2]*m + [1]*(n-m))
    res.m = np.array([1]*n)
    sz = res.n * res.m
    b = v.reshape([2]*m, order='F').reshape(sz, order='F')
    res.tt = tt.vector(b, eps, rmax)
    return res


class Clock:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        # print(self.name)
        self.begin = time.clock()
        return self

    @property
    def current(self):
        return time.clock() - self.begin


    def __exit__(self, exception_type, exception_value, traceback):
        pass
        # print(time.clock() - self.begin)
