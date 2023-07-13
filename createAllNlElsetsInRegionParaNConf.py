#!/usr/bin/python

import numpy as np
import datetime
import multiprocessing
from functools import partial
from dictionary import thisdict 

def getElemInd(f, numElements, elemCent, dr):
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

def multiprocessing_func(fip, ijk):
    print (str(fip+1) + '/' + str(total))

    elemInd = getElemInd(fip, numElements, elemCent, dr)

    return elemInd

################################################################
################# start main Program ##########################
###############################################################
if __name__ == '__main__':

    ###############################
    ######   USER INPUTS  #########
    ###############################

    # input deck name without .inp (i.e., the output of this script)
    deckName = thisdict["deckName"]

    # element Set name
    elsetName = 'nlFip'

    #length of edge of square nl volume
    dx = 0.215443469

    # radius of equivelent volume 
    dr = ((3./4.)*dx**3./np.pi)**(1./3.)

    #number of processors
    numProc = 4

    ###############################
    ######   LOAD FILES   #########
    ###############################

    #abaqus output files
    elsetFile = deckName + '-Elsets.inp'
    fileOutput = open(elsetFile ,'w')

    elsetMatFile = deckName + '-ElsetsMat.inp'
    fileOutput2 = open(elsetMatFile ,'w')

    elsetCentRFile = deckName + '-ElsetsCentR.inp'
    fileOutput3 = open(elsetCentRFile ,'w')

    # node file name (from getElsetNode getElsetNodesElems.py, getNlNodesElems.py)
    nodeFile = 'nlNodes.inp'
    # element file name
    elementFile = 'nlElements.inp'
    # elset file name
    elsetFile = 'nlElsets.inp'

    # centroids of elems from getElemCent.py
    elemCentFile = deckName +'-ElemCent.inp'

    ## Open input files
    nodes = np.loadtxt(nodeFile,delimiter=',')
    elements = np.loadtxt(elementFile,delimiter=',',dtype=int)
    elemCent = np.loadtxt(elemCentFile,delimiter=',')
    matrixElset = np.loadtxt(elsetFile,dtype=int)
    matrixElsetInd = matrixElset-1

    # assumes element numbers start at 1 with no breaks

    if matrixElsetInd:
        elements = elements[matrixElsetInd,:]

    numNodes = nodes.shape[0]
    print ('Number of Nodes: ' + str(numNodes))

    numElements = elements.shape[0]
    nodesPerElem = elements.shape[1] - 1
    print ('Number of Elements: ' + str(numElements))
    print ('Number of Nodes per  Elements: ' + str(nodesPerElem))
    print(deckName)

    fipCount = 1
    print ('start fip count           : ' + str(datetime.datetime.now()))


    #####################################################################
    ###################### find elements in irregular mesh ##############
    #####################################################################
    total = numElements
    #total = 1000
    
    pool = multiprocessing.Pool(processes = numProc)
    elemIndArray = pool.map(partial(multiprocessing_func,ijk=range(total)), range(total))

    sizeElemInd = 0

    for fipCount in range(total):

        elemIndTemp = elemIndArray[fipCount]
        elemInd = elemIndTemp[0:-1:2]
        elemCentR = elemIndTemp[1:len(elemIndTemp):2]
        #print elemInd
        #print elemCentR
        if len(elemInd) > sizeElemInd:
            sizeElemInd = len(elemInd)

        #print 'start writing elements to file  : ' + str(datetime.datetime.now())
        fileOutput.write('\n' + '*Elset, elset=' + elsetName + str(fipCount+1) + '\n')

        for i in range(len(elemInd)):
            fileOutput.write(str(int(elemInd[i])) + ', ')
            if i != 0 and i % 15 == 0:
                fileOutput.write('\n')        
        #print 'end writing elements to file    : ' + str(datetime.datetime.now())                         
        #if len(elemInd) < 20:
        #    print elemInd

    elsetMat = np.zeros((total,sizeElemInd))         
    elsetCentRMat = np.zeros((total,sizeElemInd))         
    elsetCentRMat[:] = np.nan
    for fipCount in range(total):
        elemIndTemp = elemIndArray[fipCount]
        elemInd = elemIndTemp[0:-1:2]
        elemCentR = elemIndTemp[1:len(elemIndTemp):2]

        for i in range(len(elemInd)):
            #print len(elemInd)
            elsetMat[fipCount,i] = int(elemInd[i])
            elsetCentRMat[fipCount,i] = elemCentR[i]
    for fipCount in range(total):    
        for i in range(sizeElemInd):
            if i == (sizeElemInd - 1 ):
                fileOutput2.write(str(int(elsetMat[fipCount,i])))
                fileOutput3.write(str((elsetCentRMat[fipCount,i])))
            else:
                fileOutput2.write(str(int(elsetMat[fipCount,i])) + ', ')
                fileOutput3.write(str((elsetCentRMat[fipCount,i])) + ', ')
        fileOutput2.write('\n')
        fileOutput3.write('\n')

    print ('end fip count           : ' + str(datetime.datetime.now()))

    fileOutput.close()
    fileOutput2.close()
    fileOutput3.close()

