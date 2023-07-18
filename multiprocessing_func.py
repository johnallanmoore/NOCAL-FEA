# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 14:26:48 2023

@author: chandela
"""

def multiprocessing_func(fip, ijk, total, numElements,elemCent, dr):
    
    from getElemInd import getElemInd
    
    print ((str(fip + 1)) + '/' + str(total))

    elemInd = getElemInd(fip, numElements, elemCent, dr)

    print("this is the name of the function:" + __name__)
    
    return elemInd
