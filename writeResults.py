dataPath = './data/'
testFileName = 'testData.txt'

numElems = 11*11*11

numCol = 3

outputValue = 1.23456789

outputfilename=dataPath+testFileName
out = open(outputfilename,'w')

for i in range(numElems):

    out.write(str(i+1))
    for j in range(numCol):
        out.write(', ' + str(outputValue))
    if i != numElems -1:
        out.write('\n')

out.close()
