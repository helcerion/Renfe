#-------------------------------------------------------------------------------
# Name:        renfe
#
# Author:      Albert
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from HTMLParser import HTMLParser
import urllib2
from urllib import urlencode
import re
import time

class MyHTMLParser(HTMLParser):
    body = 0
    texto = ""
    resultado = []
    def handle_starttag(self, tag, attrs):
        #if tag == "tr":
        #    print ''
        #elif tag == "td":
        #    print self.get_starttag_text(),
        if tag == "td": #if tag == "tbody":
            self.body = 1
        pass

    def handle_endtag(self, tag):
        #if tag == "td":
        #    print "</td>",
        if tag == "td": #"tbody":
            self.body = 0
        if self.body == 1:
            if tag == 'tr':
                self.resultado.append(self.texto.strip())
                self.texto = ""
        pass

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self.body == 1:
            string = data.strip()
            if string != "":
                self.texto = self.texto + data + " "
        pass

    def getResultado(self):
        return self.resultado

def main():
    now = time.strftime("%H", time.localtime())
    later = int(now) + 1
    day = time.strftime("%d",  time.localtime())
    month = time.strftime("%m",  time.localtime())
    year = time.strftime("%Y",  time.localtime())
    values = {'day': day,  'month': month,  'year': year,'sourceCode': '78805', 'destinationCode': '79500', 'fromtime': now, 'totime': later} #pl catalunya:78805, mataro:79500, sants:71801, sant adria:79403, (horariDesde, horariFins + nomes hora)
    data = urlencode(values)
    url = "http://www14.gencat.cat/mobi_rodalies/AppJava/pages/horaris/ResultatCerca.htm"

    req = urllib2.Request(url, data)
    f = urllib2.urlopen(req)
    p = MyHTMLParser()
    page = f.read()
    f.close()

    horaris_start = page.find('class="timetablesTable"')
    horaris_stop = page.find('</ul>',horaris_start)
    taula = page[horaris_start:horaris_stop]

    p.feed(taula)
    resultado = p.getResultado()
    for fila in resultado:
        print fila

    pass

if __name__ == '__main__':
    main()
