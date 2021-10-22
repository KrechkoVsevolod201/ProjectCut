# fileName = ""

def openAndAppend():
    f = open('D:\PycharmProjects\ProjectCut\AsistFiles\Help.txt', 'r')
    fileName = f.read()
    f.close()
    print(fileName)
    f = open('D:\PycharmProjects\ProjectCut\DATABase\DirectoryHistory.txt', 'a')
    f.write(fileName + '\n')
    f.close()

openAndAppend()