#-------------------------------------------------------------------------------
# Name:        web_parser
#
# Author:      Albert
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from HTMLParser import HTMLParser
from dom_element import DOMElement
import urllib2
from urllib import urlencode


class WebParser(HTMLParser):
    dom = None
    currentElement = None
    body = 0

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.body = 1
            self.dom = DOMElement(tag='html')
            self.currentElement = self.dom
        if self.body == 1:
            elem = DOMElement(tag=tag)
            elem.set_attrs(dict(attrs))
            self.currentElement.add_children(elem)
            self.currentElement = elem

    def handle_endtag(self, tag):
        if tag == "body":
            self.body = 0
        if self.body == 1:
            elem = self.currentElement.get_parent()
            self.currentElement = elem

    def handle_startendtag(self, tag, attrs):
        if self.body == 1:
            elem = DOMElement(tag=tag)
            elem.set_attrs(dict(attrs))
            self.currentElement.add_children(elem)

    def handle_data(self, data):
        if self.body == 1:
            self.currentElement.set_text(data)
