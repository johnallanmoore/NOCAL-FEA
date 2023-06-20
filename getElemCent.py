#!/usr/bin/python

import numpy as np
import datetime


################################################################
################# start main Program ##########################
###############################################################
if __name__ == '__main__':

    ###############################
    ######   USER INPUTS  #########
    ###############################

    # input deck name without .inp (i.e., the output of this script)
    deckName = 'paraFipMesh_11'

    ###############################
    ######   LOAD FILES   #########
    ###############################

    #abaqus output files
    elcentFile = deckName + '-ElemCent.inp'
    fileOutput = open(elcentFile ,'w')

    # node file name (from getElsetNode getElsetNodesElems.py, getNlNodesElems.py)
    nodeFile = 'nlNodes.inp'
    # element file name
    elementFile = 'nlElements.inp'

    ## Open input files
    nodes = np.loadtxt(nodeFile,delimiter=',')
    elements = np.loadtxt(elementFile,delimiter=',',dtype=int)

    numNodes = nodes.shape[0]
    print ('Number of Nodes: ' + str(numNodes))

    numElements = elements.shape[0]
    nodesPerElem = elements.shape[1] - 1
    print ('Number of Elements: ' + str(numElements))
    print ('Number of Nodes per  Elements: ' + str(nodesPerElem))

    for e in range(numElements):
        ind = elements[e,1:10]
        nodesInElem =  nodes[ind-1,1:4]
        xCent = 0.0
        yCent = 0.0
        zCent = 0.0
        for i in range(nodesPerElem):
            xyz = nodesInElem[i]
            xCent = xCent + xyz[0]
            yCent = yCent + xyz[1]
            zCent = zCent + xyz[2]
        xCent = xCent/nodesPerElem
        yCent = yCent/nodesPerElem
        zCent = zCent/nodesPerElem
        fileOutput.write(str(e+1) + ', ' + str(xCent) +  ', ' + str(yCent) + ', ' + str(zCent) + '\n')

    fileOutput.close()


