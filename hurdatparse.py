import csv
import geopy
import datetime
import shapely
import numpy
import copy
from datetime import date
from geopy import distance
from shapely.geometry import Polygon, Point
from numpy import arange


hurdatFile = open('weatherparsing/hurdat2.csv')
windOutputFile = open('weatherparsing/hurWind_0_3.csv','w')
hurdatReader = csv.reader(hurdatFile)
curStormName = 'Unknown'
minLat = 20.0
maxLat = 40.0
minLon = -100.0
maxLon = -75.0
resolution = 0.3
output = []
for row in hurdatReader:
        if row[0].startswith("AL"):
            curStormName = row[1]
        else:
            curHur = {}
            curHur['stormName'] = curStormName.strip()
            curHur['year'] = int(row[0][:4])
            curHur['month'] = int(row[0][4:6])
            curHur['day'] = int(row[0][6:8])
            curDate = date(curHur['year'],curHur['month'],curHur['day'])
            print(curDate)
            curHur['weekOfYear'] = curDate.isocalendar()[1]
            curHur['dayOfYear'] = curDate.timetuple().tm_yday
            curHur['time'] = row[1]
            curHur['type'] = row[3]
            curHur['eyeLat'] = float(row[4].replace('N',''))
            curHur['eyeLon'] = -float(row[5].replace('W','').replace('E',''))
            curHur['maxWind'] = float(row[6])
            curHur['minPressure'] = float(row[7])
            if(float(row[8]) > 0):
                ne34 = distance.distance(nautical=float(row[8])).destination((curHur['eyeLat'],curHur['eyeLon']),45)
                se34 = distance.distance(nautical=float(row[9])).destination((curHur['eyeLat'],curHur['eyeLon']),135)
                sw34 = distance.distance(nautical=float(row[10])).destination((curHur['eyeLat'],curHur['eyeLon']),225)
                nw34 = distance.distance(nautical=float(row[11])).destination((curHur['eyeLat'],curHur['eyeLon']),315)
            
                ne50 = distance.distance(nautical=float(row[12])).destination((curHur['eyeLat'],curHur['eyeLon']),45)
                se50 = distance.distance(nautical=float(row[13])).destination((curHur['eyeLat'],curHur['eyeLon']),135)
                sw50 = distance.distance(nautical=float(row[14])).destination((curHur['eyeLat'],curHur['eyeLon']),225)
                nw50 = distance.distance(nautical=float(row[15])).destination((curHur['eyeLat'],curHur['eyeLon']),315)

                ne64 = distance.distance(nautical=float(row[16])).destination((curHur['eyeLat'],curHur['eyeLon']),45)
                se64 = distance.distance(nautical=float(row[17])).destination((curHur['eyeLat'],curHur['eyeLon']),135)
                sw64 = distance.distance(nautical=float(row[18])).destination((curHur['eyeLat'],curHur['eyeLon']),225)
                nw64 = distance.distance(nautical=float(row[19])).destination((curHur['eyeLat'],curHur['eyeLon']),315)

                # Define polys
                poly34 = Polygon(((ne34.latitude,ne34.longitude),(se34.latitude,se34.longitude),(sw34.latitude,sw34.longitude),(nw34.latitude,nw34.longitude)))
                poly50 = Polygon(((ne50.latitude,ne50.longitude),(se50.latitude,se50.longitude),(sw50.latitude,sw50.longitude),(nw50.latitude,nw50.longitude)))
                poly64 = Polygon(((ne64.latitude,ne64.longitude),(se64.latitude,se64.longitude),(sw64.latitude,sw64.longitude),(nw64.latitude,nw64.longitude)))

                # Check points within our bounding box
                for curLat in arange(minLat,maxLat,resolution):
                    for curLon in arange(minLon,maxLon,resolution):
                        curPoint = Point(curLat,curLon)
                        gotMatch = False
                        # Expanding speeds
                        if poly64.contains(curPoint):
                            curHur['wind']  = 64
                            gotMatch = True
                        else:
                            if poly50.contains(curPoint):
                                curHur['wind'] = 50
                                gotMatch = True
                            else:
                                if poly34.contains(curPoint):
                                    curHur['wind'] = 34
                                    gotMatch = True
                        if gotMatch:
                            curHur['lat'] = curLat
                            curHur['lon'] = curLon
                            output.append(copy.deepcopy(curHur))
                            #print(f"{curHur['lat']},{curHur['lon']} -> {curHur['wind']}")
print("Writing to file")
cw = csv.DictWriter(windOutputFile,fieldnames=output[0].keys())
cw.writeheader()
cw.writerows(output)
