import sys
sys.path.append("tools")
from tools.Object import *
from parameters import *


for star in stars:
    print(star)
    ObservedObject(star, "parameters.py")
    print(50*"=")
