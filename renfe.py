#-------------------------------------------------------------------------------
# Name:        renfe
#
# Author:      Albert
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from web_parser import WebParser
import urllib2
from urllib import urlencode
import re
import time

def main():
    line_train = stations()
    i = 0
    for station_id in line_train.keys():
        print station_id, '-', line_train[station_id]
    station = raw_input('Enter the station ID for destination: ')
    arrival = raw_input('Enter the arrival time (HH.MM format): ')
    arrivalTime = time.strptime(str(arrival), '%H.%M')
    schedules = schedule(station, arrivalTime.tm_hour)
    departure_time_result = time.strptime(str(int(arrivalTime.tm_hour) - 2)+".00", '%H.%M')
    arrival_time_result = ''
    for row in schedules.values():
        aux_arrival_time = time.strptime(row['arrivalTime'], '%H.%M')
        if aux_arrival_time < arrivalTime and aux_arrival_time > departure_time_result:
            departure_time_result = aux_arrival_time
            arrival_time_result = row['departureTime']
            trip_time_result = row['tripTime']
    print "Departure:", arrival_time_result, "- Arrival:", str(departure_time_result.tm_hour) + "." + str(departure_time_result.tm_min), "- Trip:", trip_time_result

def get_page(url, data):
    req = urllib2.Request(url, data)
    f = urllib2.urlopen(req)
    page = f.read()
    f.close()
    return page

def stations():
    values = {'lineId': 'R1'}
    data = urlencode(values)
    url = "http://www14.gencat.cat/mobi_rodalies/AppJava/pages/linies/Detall.htm"
    page = get_page(url, data)
    p = WebParser()
    p.feed(page)
    station_list = p.dom.getElementsByClass('RodaliesList')[0]
    station_list = station_list.getElementsByTag('li')
    result = {}
    for sl in station_list:
        id = sl.get_id()[9:]
        station_name_elem = sl.getElementsByClass('stationName')[0]
        station_name_elem = station_name_elem.getElementsByTag('xml-fragment')[0]
        station_name = station_name_elem.get_text()
        result[id] = station_name
    return result
    
def schedule(destination, now):
    now = int(now) - 1
    later = int(now) + 1
    day = time.strftime("%d",  time.localtime())
    month = time.strftime("%m",  time.localtime())
    year = time.strftime("%Y",  time.localtime())
    values = {'day': day,  'month': month,  'year': year,'sourceCode': '79500', 'destinationCode': destination, 'fromtime': now, 'totime': later} #pl catalunya:78805, mataro:79500, sants:71801, sant adria:79403, (horariDesde, horariFins + nomes hora)
    data = urlencode(values)
    url = "http://www14.gencat.cat/mobi_rodalies/AppJava/pages/horaris/ResultatCerca.htm"
    
    page = get_page(url, data)
    
    p = WebParser()
    p.feed(page)
    
    timetables = p.dom.getElementById('timetablesTable')
    schedules = timetables.getElementsByTag('li')
    
    timeTable = {}
    
    for schedule in schedules:
        id = schedule.get_id()
        departure = schedule.getElementsByClass('departureTime')
        arrival = schedule.getElementsByClass('arrivalTime')
        triptime = schedule.getElementById('tripTimeText')
        if departure != [] or arrival != []:
            timeTable[id] = {'departureTime': departure[0].get_text(), 'arrivalTime': arrival[0].get_text(), 'tripTime': triptime.get_text()}
    return timeTable

if __name__ == '__main__':
    main()
