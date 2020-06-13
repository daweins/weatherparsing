import time
import re
import datetime
minYear = 1980
maxYear = 2019

for curYear in range(minYear,maxYear):
    startDate = datetime.date(curYear,6,1)
    endDate = datetime.date(curYear,12,1)
    curDate = startDate
    while curDate < endDate:
        print(curDate)
        curDate = curDate + datetime.timedelta(days=7)
    
    