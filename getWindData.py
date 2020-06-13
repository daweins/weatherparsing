import requests
import json
import time
import csv
import datetime

token = "UzStCJRhneunWnaXRdHziwobKkuXqeSl"

templateURL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=FIPS:12&limit=1000&datatypeid=AWND&units=standard"
headerList = {}
headerList["token"] = token

minYear = 2004
maxYear = 2005
dayIncrement=7
data_file = open('test3.csv','a+')
       
for curYear in range(minYear,maxYear):
    startDate = datetime.date(curYear,6,1)
    endDate = datetime.date(curYear,12,1)
    curDate = startDate
    while curDate < endDate:
        nextDate = curDate + datetime.timedelta(days=dayIncrement)
        curURL = templateURL + "&startdate="+curDate.strftime("%Y-%m-%d")+"&enddate="+nextDate.strftime("%Y-%m-%d")
        print(curURL)
        curDate = nextDate
        try:
            response = requests.get(curURL, headers=headerList)
            responseJSON = json.loads(response.content)
            windData = responseJSON["results"]
            csv_writer = csv.writer(data_file)
            count=0
            for curResult in windData:
                if count == 0:
                    header = curResult.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(curResult.values())
        except:
            print("Error")
data_file.close()



