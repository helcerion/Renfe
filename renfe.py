# ------------------------------------------------------------------------------
# Name:        renfe
#
# Author:      Albert
# ------------------------------------------------------------------------------
#!/usr/bin/env python

from web_parser import WebParser
import urllib2
from urllib import urlencode
import time


def main():
    line_train = stations()
    for station_id in line_train.keys():
        print station_id, '-', line_train[station_id]
    station = raw_input('Enter the station ID for destination: ')
    arrival = raw_input('Enter the arrival time (HH.MM format): ')
    arrival_time = time.strptime(str(arrival), '%H.%M')
    schedules = schedule(station, arrival_time.tm_hour)
    departure_time_result = time.strptime(str(int(arrival_time.tm_hour) - 2) + ".00", '%H.%M')
    arrival_time_result = ''
    trip_time_result = ''
    for row in schedules.values():
        aux_arrival_time = time.strptime(row['arrivalTime'], '%H.%M')
        if departure_time_result < aux_arrival_time < arrival_time:
            departure_time_result = aux_arrival_time
            arrival_time_result = row['departureTime']
            trip_time_result = row['tripTime']
    print "Departure:", arrival_time_result, "- Arrival:", str(departure_time_result.tm_hour) + "." + str(
        departure_time_result.tm_min), "- Trip:", trip_time_result


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
    station_list = p.dom.get_elements_by_class('RodaliesList')[0]
    station_list = station_list.get_elements_by_tag('li')
    result = {}
    for sl in station_list:
        station_id = sl.get_id()[9:]
        station_name_elem = sl.get_elements_by_class('stationName')[0]
        station_name_elem = station_name_elem.get_elements_by_tag('xml-fragment')[0]
        station_name = station_name_elem.get_text()
        result[station_id] = station_name
    return result


def schedule(destination, now):
    now = int(now) - 1
    later = int(now) + 1
    day = time.strftime("%d",  time.localtime())
    month = time.strftime("%m",  time.localtime())
    year = time.strftime("%Y",  time.localtime())
    # pl catalunya:78805, mataro:79500, sants:71801, sant adria:79403, (horariDesde, horariFins + nomes hora)
    values = {'day': day, 'month': month, 'year': year, 'sourceCode': '79500', 'destinationCode': destination,
              'fromtime': now, 'totime': later}

    data = urlencode(values)
    url = "http://www14.gencat.cat/mobi_rodalies/AppJava/pages/horaris/ResultatCerca.htm"

    page = get_page(url, data)

    p = WebParser()
    p.feed(page)

    timetables = p.dom.get_element_by_id('timetablesTable')
    schedules = timetables.get_elements_by_tag('li')

    time_table = {}

    for schedule_item in schedules:
        item_id = schedule_item.get_id()
        departure = schedule_item.get_elements_by_class('departureTime')
        arrival = schedule_item.get_elements_by_class('arrivalTime')
        triptime = schedule_item.get_element_by_id('tripTimeText')
        if departure != [] or arrival != []:
            time_table[item_id] = {'departureTime': departure[0].get_text(), 'arrivalTime': arrival[0].get_text(),
                                   'tripTime': triptime.get_text()}
    return time_table

if __name__ == '__main__':
    main()
