# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:24:31 2023

@author: chandela
"""

from getNlNodesElems import getNlNodesElem
from getElemCent import getElemCent
from runNonlocalFip import runNonlocalFip
from createAllNlElsetsInRegionParaNConftest import createVolume
from dictionary import thisdict 

if __name__=="__main__":
    getNlNodesElem()
    getElemCent()
    createVolume()
    runNonlocalFip()
    
