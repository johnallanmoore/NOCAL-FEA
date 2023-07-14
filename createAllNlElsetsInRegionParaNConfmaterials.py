# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 14:19:45 2023

@author: chandela
"""

def getElemInd(f, numElements, elemCent, dr):
    
    import numpy as np
    import datetime
    import multiprocessing
    from functools import partial
    from dictionary import thisdict 
    import sys
    
    # f is the counter for the nonlocal volume
    elemInd = np.empty((numElements,2))
    elemInd[:] = np.nan

    counter = 0

    x0 = elemCent[f,1]
    y0 = elemCent[f,2]
    z0 = elemCent[f,3]

    for e in range(numElements):
        xP = elemCent[e,1]
        yP = elemCent[e,2]
        zP = elemCent[e,3]

        x1 = abs(xP - x0);
        y1 = abs(yP - y0);
        z1 = abs(zP - z0);

        r = np.sqrt(x1**2. + y1**2. +z1**2.);
        if r <= dr:
            elemInd[counter,0] = elemCent[e,0]
            elemInd[counter,1] = r
            counter = counter + 1

    elemInd = elemInd[~np.isnan(elemInd)]
    #elemInd = elemInd.astype(np.int64)

    return elemInd

def multiprocessing_func(fip, ijk, total, numElements,elemCent, dr):
    
    print (str(fip+1) + '/' + str(total))

    elemInd = getElemInd(fip, numElements, elemCent, dr)

    return elemInd