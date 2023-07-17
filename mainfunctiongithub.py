# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:24:31 2023

@author: chandela
"""

from getNlNodesElems import getNlNodesElem
from getElemCent import getElemCent
#from createAllNlElsetsInRegionParaNConf import getElemInd
#from createAllNlElsetsInRegionParaNConf import multiprocessing_func
#from runNonlocalFip import runNonlocalFip
from createAllNlElsetsInRegionParaNConftest import main
from dictionary import thisdict 
import numpy as np

getNlNodesElem()
getElemCent()
main()
#runNonlocalFip()
#getElemInd(f, numElements, elemCent, dr)
#multiprocessing_func(fip, ijk, total, numElements, elemCent, dr)

def foo():
    from multiprocessing_func import multiprocessing_func

    MP = multiprocessing_func(fip, ijk, total, numElements, elemCent, dr)
    result = MP.run()

print(__name__)

if __name__ == '__main__':
    total = 1331
    fip = range(total)
    ijk = range(total)
    numElements = 1331
    dr = 0.1336
    deckName = thisdict["deckName"]
    elemCentFile = deckName +'-ElemCent.inp'
    elemCent = np.loadtxt(elemCentFile,delimiter=',')
    foo()  
    
main()
