def nonlocalFIPWeight():
    import math
    import datetime

    import numpy as np
    import sys

    dataPath = './data/'
    resultsPath = './results/'

    deckName = 'paraFipMesh_11'

    resultsFileName = 'paraFipMesh-FIP_1_11.txt'

    print('nonlocal post processing ' + resultsFileName)

    # length scale
    L = 0.13365046175

    outputfilename1=resultsPath+resultsFileName+'-nonlocalFIP_NCW.txt'
    

    ## open txt file to write to
    out1 = open(outputfilename1,'w')
    elsetsFile = deckName +'-ElsetsMat.inp'

    elsetsMat = np.loadtxt(elsetsFile,delimiter=',',dtype=int)

    elsetsCentRFile = deckName +'-ElsetsCentR.inp'
    elsetsCentR = np.loadtxt(elsetsCentRFile,delimiter=',')


    numVols = len(elsetsMat[:,0])

    fipFile = dataPath + resultsFileName
    localFipMat = np.loadtxt(fipFile,delimiter=',')

    numSteps = len(localFipMat[0,:])-1
    numElem  = len(localFipMat[:,0])


    nonlocalFipMat = np.zeros((numVols,numSteps))

    for s in range(numSteps):
            print('start step ' + str(s+1))
            for f in range(numVols):
                    elset = elsetsMat[f,:]
                    elset = elset[np.nonzero(elset)]
                    centR = elsetsCentR[f,:]
                    centR = centR[~np.isnan(centR)]
                    # assumes all element in volume are roughly the same size
                    numElemVol = len(elset)

                    sumVal = 0
                    Ax = 0
                    counter = 0
                    for e in elset:
                            elemInd = np.where(localFipMat[:,0] == e)
                            phi = np.exp(-centR[counter]**2.0/L**2.0)
                            counter = counter + 1
                            for gp in elemInd:
                                    sumVal += localFipMat[gp,s+1]*phi
                                    Ax += phi
                    aveVal = sumVal/Ax
                    nonlocalFipMat[f,s] = aveVal

    # write data

    for f in range(numVols):
            for s in range(numSteps):
                    if s == numSteps-1:
                            out1.write(str(nonlocalFipMat[f,s]))
                    else:
                            out1.write(str(nonlocalFipMat[f,s]) + ', ')
            out1.write('\n')

    print("max fip in last step" + str(max(nonlocalFipMat[:,-1])))


    # close input and output files
    out1.close()



