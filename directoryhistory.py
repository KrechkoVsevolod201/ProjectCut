from datetime import datetime

def openAndAppend():
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second

    datetimestr = (year + month + day + hour + minute + second)
    print(datetimestr)
    f = open('D:\PycharmProjects\ProjectCut\AsistFiles\FileWay.txt', 'r')
    fileName = f.read()
    f.close()
    print(fileName)
    f = open('D:\PycharmProjects\ProjectCut\DATABase\DirectoryHistory.txt', 'a')
    f.write(fileName + '\n')
    f.close()

openAndAppend()