#!/usr/bin/python
def getNlNodesElem():
    
    import numpy as np
    from dictionary import thisdict 
    
    dataPath = './data/'
    
    # mesh input file (user input)
    #neperInput = 'paraFipMesh_11.inp'
    #neperInput = 'paraFipMesh_19.inp'
    #neperInput = 'paraFipMesh_32.inp'
    neperInput = thisdict["neperInput"]
    
    #abaqus output files (these always stay the same)
    nodeFile = 'nlNodes.inp'
    elementFile = 'nlElements.inp'
    elsetFile = 'nlElsets.inp'
    nsetFile = 'nlNsets.inp'
    numNsetsFile = 'nlNumNsets.inp'
    numElsetsFile = 'nlNumElsets.inp'
    
    
    fileInput = open(dataPath + neperInput,'r')
    
    counter = 0
    counterElem = 0
    counterElset = 0
    counterNset = 0
    
    firstNset = True
    firstLine = False
    firstElset = True
    isElset = False
    isElem = False
    
    for line in fileInput:
        words = line.split()
        if counter < 40000000000:
            try:
                if f.closed == False:
                    if isElem == True:
                        counterElem = counterElem + 1
            except:
                pass
            #this checks if there is anything in the lines
            if words:
                # len(words) protects against *Node Output card
                if words[0].lower() == '*node' and len(words) == 1:
                    print( 'its a node')
                    # if its the node card open nlNodes.inp
                    f = open(nodeFile,'w')
                    firstLine = True
                    isElset = False
                    isElem = False
                elif words[0].lower() == '*element,':
                    print ('its an element')
                    # if its the element card open nlElements.inp
                    f = open(elementFile,'w')
                    firstLine = True
                    isElset = False
                    isElem = True
                elif words[0].lower() == '*elset,' and firstElset == True :
                    # determine if its explicit element numner or 
                    # the generate command
                    if words[1].lower() == 'elset=matrix,' :
                        if words[2].lower() == 'generate':
                            isGenerate = True
                        else:
                            isGenerate = False
                    elif words[1].lower() == 'elset=matrix' :
                        isGenerate = False
                    else:
                        print ("first element set must be called Matrix")
                    
                    firstLine = True
    
                    print ('its the first element set')
                    f = open(elsetFile,'w')
                    isElset = True
                    isElem = False
                    numElemInGrain = 0
                    firstElset = False
                        
                        # write the elset card
                        # skip the carriage return and add some Abaaqus stuff
                        # use this one if the elsets are define after the istance
                        #f.write(line[0:-1] + ', internal, instance=Part-1-1' + '\n' )
                        # use this one if the elsets are define in the part)
                        #f.write(line[0:-1]  + '\n' )
                    counterElset = counterElset + 1
    
                elif words[0].lower() == '*nset,':
                    firstLine = True
                    isElset = False
                    isElem = False
                    if firstNset == True:
                        print ('its the first node set')
                        f = open(nsetFile,'w')
                        firstNset = False
                    else:
                        f = open(nsetFile,'a')
    
                    # write the nset card
                    # skip the carriage return and add some Abaaqus stuff
                    #f.write(line[0:-1] + ', internal, instance=Part-1-1' + '\n' )
                    counterNset = counterNset + 1
    
                # close the output file if the card is something uneeded
                elif words[0] == '**':
                    try:
                        f.close() 
                    except:
                        pass
                elif words[0].lower() == '*solid':
                    f.close() 
                elif words[0].lower() == '*end':
                    f.close() 
                elif words[0].lower() == '*material':
                    f.close()  
                elif words[0].lower() == '*boundary':
                    f.close() 
                elif words[0].lower() == '*step':
                    f.close()             
                elif words[0].lower() == '*elset,' and firstElset == False :
                    f.close()             
            else:
                try:
                    f.close()
                except:
                    pass
    
            try:
                if f.closed == False:
                    # if a file is open
                    if firstLine == True:
                        # this skips the card line
                        firstLine = False
                    else:
                        # write out elsets elements in a column
                        if isElset == True:
                            if isGenerate == True:
                                w = words[0]
                                eLim = np.fromstring(w,sep=',',dtype=int)
                                for kk in range(eLim[0],eLim[1]+1):
                                    f.write(str(kk)+'\n')
                            else:
                                for w in words:
                                    warray = np.fromstring(w,sep=',',dtype=int)
                                    for kk in range(len(warray)):
                                    #                                if w[kk] != ',':
                                        f.write(str(warray[kk])+'\n')
                            #isElset = False
                            #f.close() # so it only collects first elset data
            #                                if w[-1] == ',':
            #                                    f.write(w[0:-1]+'\n')
            #                                else:
            #                                    f.write(w+'\n')
        
                        else:
                            # if its not an elset, just write the line to the file
                            f.write(line)
            except:
                pass
        counter = counter + 1
    
    print ('there are ' + str(counterElem-1) + ' elements')
    
    # write number of nsets and elsets to files
    print ('there are ' + str(counterNset) + ' node sets')
    fnset = open(numNsetsFile,'w') 
    fnset.write(str(counterNset))
    fnset.close()
    
    print ('there are ' + str(counterElset) + ' element sets')
    felset = open(numElsetsFile,'w') 
    felset.write(str(counterElset))
    felset.close()
    
    f.close()
    fileInput.close()
    
