# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:24:31 2023

@author: chandela
"""

#USE THIS ONE - ayushi

from getNlNodesElems import getNlNodesElem
from getElemCent import getElemCent
from runNonlocalFip import runNonlocalFip
from createAllNlElsetsInRegionParaNConftest import createVolume
from plot import plotNl
from dictionary import thisdict 

if __name__=="__main__":
    runOnly = thisdict['runOnly']
    if runOnly.lower() == 'getnlnodeselem': 
        getNlNodesElem()
    elif runOnly.lower() == 'getelemcent':
        getElemCent()
    elif runOnly.lower() == 'createvolume':
        createVolume()
    elif runOnly.lower() == 'plotnl':
        plotNl()
    elif runOnly.lower() == 'runnonlocalfip':
        runNonlocalFip()
    else:
        getNlNodesElem()
        getElemCent()
        createVolume()
        plotNl()
        runNonlocalFip()
