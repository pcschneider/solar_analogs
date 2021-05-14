import numpy as np

def get_filename(fn, parameter):
    parameters = __import__(fn[0:-3])
    pm = getattr(parameters, parameter)
    return pm

def get4(fn, parameter, key="target"):
    tbl = Table.read(fn, format='ascii.ecsv', delimiter=';')
    return dict({x:tbl[parameter][i] for i,x in enumerate(tbl[key])})


class Object_Params:
    def __init__(self, fn):
        self.filename = fn
    def source_position(self, target):
        fn = get_filename(self.filename, "extract_prop_fn")
        x, y = get4(fn, "src_x"), get4(fn, "src_y")
        return x, y
    
if __name__ == "__main__":
    o = Object_Params("parameters.py")
    print(o.source_position("HD 42618"))
