import numpy as np
from astropy.table import Table

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
    def source_position_xy(self, target):
        fn = get_filename(self.filename, "extract_prop_fn")
        x, y = get4(fn, "src_x")[target], get4(fn, "src_y")[target]
        return x, y
    def 
    
if __name__ == "__main__":
    o = Object_Params("parameters.py")
    print(o.source_position_xy("HD 42618"))
