#!/usr/bin/python

import numpy as np
import datetime
#import multiprocessing
from functools import partial
import dask
import dask.array as da
import time
from dask.distributed import Client
from dask_jobqueue import SLURMCluster

def getElemInd(minMaxArray,numNodes,numElements, nodes, elements,nodesPerElem):

    xMin = minMaxArray[0]
    xMax = minMaxArray[1]
    yMin = minMaxArray[2]
    yMax = minMaxArray[3]
    zMin = minMaxArray[4]
    zMax = minMaxArray[5]

    nodeInd = np.empty((numNodes,))
    nodeInd[:] = np.nan

    elemInd = np.empty((numElements,))
    elemInd[:] = np.nan

    #print 'start searching nodes           : ' + str(datetime.datetime.now())

    counter = 0
    tol = 1e-6
    for i in range(numNodes):
        xVal = nodes[i,1]
        yVal = nodes[i,2]
        zVal = nodes[i,3]

        if (xMin - tol) <=  xVal and xVal <= (xMax + tol):
            if (yMin - tol) <=  yVal and yVal <= (yMax + tol):
                if (zMin - tol) <=  zVal and zVal <= (zMax + tol):
                    nodeInd[counter] = nodes[i,0]
                    counter = counter + 1

    
    nodeInd = nodeInd[~np.isnan(nodeInd)]

    #print 'end searching nodes             : ' + str(datetime.datetime.now())
    #print 'start sorting nodes             : ' + str(datetime.datetime.now())
    nodeInd.sort()
    #print 'end sorting nodes               : ' + str(datetime.datetime.now())

    #print 'start searching elements        : ' + str(datetime.datetime.now())
    counter = 0
    for e in range(numElements):
        eElement = elements[e,1:nodesPerElem]
        for i in range(nodesPerElem-1):
            if eElement[i] in nodeInd:
                keepElement = True
                break
            else:
                keepElement = False
                break

        if keepElement:
            elemInd[counter] = elements[e,0]
            counter = counter + 1

    elemInd = elemInd[~np.isnan(elemInd)]
    elemInd = elemInd.astype(np.int64)

    return elemInd
    #print 'end searching elements          : ' + str(datetime.datetime.now())

#def multiprocessing_func(fip):
#    return range(fip)

def multiprocessing_func(fip, ijk):
    #print(str(fip+1) + '/' + str(total))

    ii = int(ijk[fip,0])
    jj = int(ijk[fip,1])
    kk = int(ijk[fip,2])
    
    xMin = x[ii]
    xMax = x[ii+1]
    yMin = y[jj]
    yMax = y[jj+1]
    zMin = z[kk]
    zMax = z[kk+1]

    minMaxArray = [xMin, xMax, yMin, yMax, zMin, zMax]

    elemInd = getElemInd(minMaxArray,numNodes,numElements, \
    nodes, elements,nodesPerElem)

    return elemInd

################################################################
################# start main Program ##########################
###############################################################
if __name__ == '__main__':

    ###############################
    ######   USER INPUTS  #########
    ###############################

    # input deck name without .inp (i.e., the output of this script)
    #deckName = 'elsetAllPost'
    deckName = 'polygranular'

    # element Set name
    elsetName = 'nlFip'

    #length of edge of square nl volume
    # fullInclusion
    #dx = 0.1
    #polygranular
    dx = 1./9.

    #number of processors/node
    numProc = 24

    #number of nodes
    numCompNodes = 3

    # Region to creat elset (for fullInclusion)
    # xGlobalMin = -0.5
    # xGlobalMax = 0.5
    # yGlobalMin = -0.5
    # yGlobalMax = 0.5
    # zGlobalMin = -0.5
    # zGlobalMax = 0.5

    xGlobalMin = 0.
    xGlobalMax = 1.
    yGlobalMin = 0.
    yGlobalMax = 1.
    zGlobalMin = 0.
    zGlobalMax = 1.

    ###############################
    ######   Dask Stuff  #########
    ###############################
    cluster = SLURMCluster(cores=numProc, processes=1, memory="16GB", walltime="02:25:00", queue="roycores", shebang="#!/bin/bash")
    cluster.scale(numCompNodes)
    client = Client(cluster)
    print(client)
    print(cluster)

    ###############################
    ######   Calc Stuff from User inPuts  #########
    ###############################

    numNlVolsx = int((xGlobalMax - xGlobalMin)/dx)
    numNlVolsy = int((yGlobalMax - yGlobalMin)/dx)
    numNlVolsz = int((zGlobalMax - zGlobalMin)/dx)

    x = np.linspace(xGlobalMin,xGlobalMax,numNlVolsx+1)
    y = np.linspace(yGlobalMin,yGlobalMax,numNlVolsy+1)
    z = np.linspace(zGlobalMin,zGlobalMax,numNlVolsz+1)

    ###############################
    ######   LOAD FILES   #########
    ###############################

    #abaqus output files
    elsetFile = deckName + '-Elsets.inp'
    fileOutput = open(elsetFile ,'w')

    elsetMatFile = deckName + '-ElsetsMat.inp'
    fileOutput2 = open(elsetMatFile ,'w')

    # node file name (from getElsetNode getElsetNodesElems.py, getNlNodesElems.py)
    nodeFile = 'nlNodes.inp'
    # element file name
    elementFile = 'nlElements.inp'
    # elset file name
    elsetFile = 'nlElsets.inp'

    ## Open input files
    nodes = np.loadtxt(nodeFile,delimiter=',')
    elements = np.loadtxt(elementFile,delimiter=',',dtype=int)
    matrixElset = np.loadtxt(elsetFile,dtype=int)
    matrixElsetInd = matrixElset-1

    # assumes element numbers start at 1 with no breaks
    elements = elements[matrixElsetInd,:]

    numNodes = nodes.shape[0]
    print('Number of Nodes: ' + str(numNodes))

    numElements = elements.shape[0]
    nodesPerElem = elements.shape[1] - 1
    print('Number of Elements: ' + str(numElements))
    print('Number of Nodes per  Elements: ' + str(nodesPerElem))

    total = numNlVolsx*numNlVolsy*numNlVolsz

    fipCount = 1
    print( 'start fip count           : ' + str(datetime.datetime.now()))

    ijkCounter = 0
    ijkVec = np.empty((total,3))

    for ii in range(numNlVolsx):
        for jj in range(numNlVolsy):
            for kk in range(numNlVolsz):
                ijkVec[ijkCounter,0] = ii
                ijkVec[ijkCounter,1] = jj
                ijkVec[ijkCounter,2] = kk            
                ijkCounter += 1

    #####################################################################
    ###################### find elements in irregular mesh ##############
    #####################################################################
    print (range(total))
    
    elemIndArray = []
    data = []


    for i in range(0,total):
        data.append(i)

    for i in data:
        j = dask.delayed(multiprocessing_func)(i,ijkVec)
        elemIndArray.append(j)

    t1 = time.time()
    elemIndArray = dask.compute(elemIndArray)
    t2 = time.time()
    elemIndArray = np.asarray(elemIndArray,dtype=object)

    print(type(elemIndArray))
    elemIndArray = elemIndArray[0]
    print(len(elemIndArray))
    print(elemIndArray.shape)
    print('Dask run time  = ' + str(t2-t1))

    sizeElemInd = 0


    for fipCount in range(total):

        elemInd = elemIndArray[fipCount]

        if len(elemInd) > sizeElemInd:
            sizeElemInd = len(elemInd)

        #print 'start writing elements to file  : ' + str(datetime.datetime.now())
        fileOutput.write('\n' + '*Elset, elset=' + elsetName + str(fipCount+1) + '\n')

        for i in range(len(elemInd)):
            fileOutput.write(str(elemInd[i]) + ', ')
            if i != 0 and i % 15 == 0:
                fileOutput.write('\n')        
        #print 'end writing elements to file    : ' + str(datetime.datetime.now())                         
        if len(elemInd) < 20:
            print(elemInd)

    elsetMat = np.zeros((total,sizeElemInd))         

    for fipCount in range(total):
        elemInd = elemIndArray[fipCount]

        for i in range(len(elemInd)):
            elsetMat[fipCount,i] = elemInd[i]

    for fipCount in range(total):    
        for i in range(sizeElemInd):
            if i == (sizeElemInd - 1 ):
                fileOutput2.write(str(int(elsetMat[fipCount,i])))
            else:
                fileOutput2.write(str(int(elsetMat[fipCount,i])) + ', ')
        fileOutput2.write('\n')

    print('end fip count           : ' + str(datetime.datetime.now()))

    fileOutput.close()
    fileOutput2.close()

