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
    now = time.strftime("%H", time.localtime())
    later = int(now) + 1
    day = time.strftime("%d",  time.localtime())
    month = time.strftime("%m",  time.localtime())
    year = time.strftime("%Y",  time.localtime())
    values = {'day': day,  'month': month,  'year': year,'sourceCode': '79500', 'destinationCode': '79403', 'fromtime': now, 'totime': later} #pl catalunya:78805, mataro:79500, sants:71801, sant adria:79403, (horariDesde, horariFins + nomes hora)
    data = urlencode(values)
    url = "http://www14.gencat.cat/mobi_rodalies/AppJava/pages/horaris/ResultatCerca.htm"

    req = urllib2.Request(url, data)
    f = urllib2.urlopen(req)
    p = WebParser()
    page = f.read()
    f.close()

    p.feed(page)
    
    timetables = p.dom.getElementById('timetablesTable')
    schedules = timetables.getElementsByTag('li')
    
    for schedule in schedules:
        id = schedule.get_id()
        departure = schedule.getElementsByClass('departureTime')
        arrival = schedule.getElementsByClass('arrivalTime')
        triptime = schedule.getElementById('tripTimeText')
        if departure != [] or arrival != []:
            print id, departure[0].get_text(), arrival[0].get_text(), triptime.get_text()

if __name__ == '__main__':
    main()
