# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:24:31 2023

@author: chandela
"""

from getNlNodesElems import getNlNodesElem
from getElemCent import getElemCent
from createAllNlElsetsInRegionParaNConf import getElemInd
from createAllNlElsetsInRegionParaNConf import multiprocessing_func
from runNonlocalFip import runNonlocalFip
from createAllNlElsetsInRegionParaNConf import createAllNlElsetsInREgionParaConf

getNlNodesElem()
getElemCent()
createAllNlElsetsInREgionParaConf()
#runNonlocalFip()
#getElemInd(f, numElements, elemCent, dr)
#multiprocessing_func(fip, ijk, total, numElements, elemCent, dr)