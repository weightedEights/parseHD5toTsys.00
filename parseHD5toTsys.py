__author__ = 'sri-Wonder'


#def calcTsys():

from tables import *


h5ds = open_file("./d0111900.dt1.h5", "r")

sysConst = h5ds.root.Rx.SysConst.read()

h5ds.close()


print sysConst