def nonlocalFIP():

    import math
    import datetime

    import numpy as np
    import sys
    from dictionary import thisdict

    resultsFileName = thisdict["resultsFileName"]

    dataPath = './data/'
    resultsPath = './results/'

    deckName = thisdict["deckName"]

    print('nonlocal post processing ' + resultsFileName)

    isNonConf = False

    if isNonConf == True:
        outputfilename1=resultsPath+resultsFileName+'-nonlocalFIP_NC.txt'
    else:
        outputfilename1=resultsPath+resultsFileName+'-nonlocalFIP_C.txt'

    ## open txt file to write to
    out1 = open(outputfilename1,'w')

    elsetsFile = deckName +'-ElsetsMat.inp'

    elsetsMat = np.loadtxt(elsetsFile,delimiter=',',dtype=int)

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

                    # assumes all element in volume are roughly the same size
                    numElemVol = len(elset)

                    sumVal = 0
                    for e in elset:
                            elemInd = np.where(localFipMat[:,0] == e)
                            for gp in elemInd:
                                    sumVal += localFipMat[gp,s+1]

                    aveVal = sumVal/numElemVol
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



