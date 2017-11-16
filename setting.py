import numpy as np
import os, yaml

class Setting:
    def __init__(self, n, dim, tau, tol, max_T, result_dir):
        self.n = n
        self.dim = dim
        self.tau = tau
        self.tol = tol
        self.N = 2**n
        self.h = 1.0/(self.N+1)
        self.result_dir = result_dir
        self.max_T = max_T
        if not os.path.exists(self.result_path()):
            os.makedirs(self.result_path())

        print("max_iter: {}".format(self.max_iter))
        print("result_path: {}".format(self.result_path()))

        with open(os.path.join(self.result_path(), 'setting.yml'), "w") as f:
            f.write(yaml.dump(self.to_dict(), default_flow_style=False))        


    def qtt_shape(self):
        return [2]*(setting.n*setting.dim)

    def result_path(self):
        return "result/{}".format(self.result_dir)

    @property
    def max_iter(self):
        return int(self.max_T/self.tau)


    def to_dict(self):
        return {
            'n':    self.n,
            'dim':  self.dim,
            'tau':  self.tau,
            'tol':  self.tol,
            'N':    self.N,
            'h':    self.h,
            'max_T':self.max_T
        } 
