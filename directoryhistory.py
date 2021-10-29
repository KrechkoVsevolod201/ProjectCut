from datetime import datetime

def openAndAppend():
    current_datetime = datetime.now()
    current_datetime = datetime.now()
    year = current_datetime.year
    yearstr = str(year)
    month = current_datetime.month
    monthstr = str(month)
    day = current_datetime.day
    daystr = str(day)
    hour = current_datetime.hour
    hourstr = str(hour)
    minute = current_datetime.minute
    minutestr = str(minute)
    second = current_datetime.second
    secondstr = str(second)

    datetimestr = (year + month + day + hour + minute + second)
    current_datetime = datetime.now()
    print(datetimestr)
    f = open('D:\PycharmProjects\ProjectCut\AsistFiles\FileWay.txt', 'r')
    fileName = f.read()
    f.close()
    print(fileName)
    f = open('D:\PycharmProjects\ProjectCut\DATABase\DirectoryHistory.txt', 'a')
    f.write(fileName + ' ')
    f.write(yearstr)
    f.write('.')
    f.write(monthstr)
    f.write('.')
    f.write(daystr)
    f.write('.')
    f.write(hourstr)
    f.write('.')
    f.write(minutestr)
    f.write('.')
    f.write(secondstr)
    f.write('\n')
    f.close()

openAndAppend()