import os, time

class Clock:
    def __init__(self, output_path=None, name=''):
        self.name = name
        self.output_path = output_path

    def __enter__(self):
        print(self.name)
        self.begin = time.clock()

    def __exit__(self, exception_type, exception_value, traceback):
        res = time.clock() - self.begin
        print(res)
        if not self.output_path == None:
            with open(os.path.join(self.output_path, '{}_time.txt'.format(self.name)), 'w') as f:
                f.write(str(res))
