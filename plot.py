def plotNl():
    import matplotlib.pyplot as plt
    import numpy as np

    from dictionary import thisdict 

    # input deck name without .inp (i.e., the output of this script)
    deckName = thisdict['deckName']

    # nonlocal element sets
    plotVolumes = thisdict['plotVolumes']
    if plotVolumes:
        vol2Plot = thisdict['vol2Plot']

        # centroids of elems from getElemCent.pya
        elemCentFile = deckName +'-ElemCent.inp'
        elemCent = np.loadtxt(elemCentFile,delimiter=',')
        x = elemCent[:,1]
        y = elemCent[:,2]
        z = elemCent[:,3]



        elsetsFile = deckName +'-ElsetsMat.inp'
        elsetsMat = np.loadtxt(elsetsFile,delimiter=',',dtype=int)
        numVols = len(elsetsMat[:,0])

        if isinstance(vol2Plot, int):
            if vol2Plot > numVols:
                print('You have selected a volume number that is greater than the max number of volumes')
                print('The max volume number is ' + str(numVols))
            elset = elsetsMat[vol2Plot,:]
            elset = elset[np.nonzero(elset)]
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.scatter(x,y,z,color=(0.1, 0.2, 0.5, 0.3))
            ax.scatter(x[elset-1],y[elset-1],z[elset-1],color=(1.0, 0.0, 0.0, 0.75))
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            try:
                fig.savefig('./results/FigureVol1.png')
            except:
                fig.savefig('../results/FigureVol1.png')
        else:
            for i in range(len(vol2Plot)):
                    if vol2Plot[i] > numVols:
                            print('You have selected a volume number that is greater than the max number of volumes')
                            print('the volume with issues is ' + str(vol2Plot[i]))
                            print('The max volume number is ' + str(numVols))
                    elset = elsetsMat[vol2Plot[i],:]
                    elset = elset[np.nonzero(elset)]
                    fig = plt.figure(i)
                    ax = fig.add_subplot(projection='3d')
                    ax.scatter(x,y,z,color=(0.1, 0.2, 0.5, 0.3))
                    ax.scatter(x[elset-1],y[elset-1],z[elset-1],color=(1.0, 0.0, 0.0, 0.75))
                    ax.set_xlabel('x')
                    ax.set_ylabel('y')
                    ax.set_zlabel('z')
                    try:
                        fig.savefig('./results/FigureVol' + str(vol2Plot[i]) + '.png')
                    except:
                        fig.savefig('../results/FigureVol' + str(vol2Plot[i]) + '.png')
        #plt.show()
