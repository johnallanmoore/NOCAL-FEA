#!/usr/bin/python

#USE THIS ONE - ayushi 

#import datetime
#import multiprocessing
#from functools import partial
#from dictionary import thisdict 

################################################################
################# start main Program ##########################
###############################################################
def createVolume():


    ###############################
    ######   USER INPUTS  #########
    ###############################
    
    import numpy as np
    import datetime
    import multiprocessing
    from functools import partial
    from dictionary import thisdict 
    import sys
    from getElemInd import getElemInd
    from multiprocessing_func import multiprocessing_func 
    import warnings
    
    # input deck name without .inp (i.e., the output of this script)
    deckName = thisdict["deckName"]

    # element Set name
    elsetName = thisdict["elsetName"]

    #length of edge of square nl volume
    dx = thisdict["dx"]

    # radius of equivelent volume 
    dr = ((3./4.)*dx**3./np.pi)**(1./3.)

    #number of processors
    numProc = thisdict["numProc"]

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
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
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

    fipCount = 1
    print ('start fip count           : ' + str(datetime.datetime.now()))


    #####################################################################
    ###################### find elements in irregular mesh ##############
    #####################################################################
    total = numElements
    #total = 1000
    
    pool = multiprocessing.Pool(processes = numProc)
    elemIndArray = pool.map(partial(multiprocessing_func,ijk=range(total), total=total, numElements=numElements, elemCent=elemCent, dr=dr), range(total))

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
    
#if __name__=="__main__":
    #main()

