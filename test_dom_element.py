import unittest
from dom_element import DOMElement

class TestDOMElement(unittest.TestCase):
    def setUp(self):
        self.de = DOMElement()
        self.div = DOMElement(tag='div')
    
    def test_createwithtag(self):
        de = DOMElement(tag='div')
        self.assertEqual("<div></div>", str(de))
    
    def test_createwithattr(self):
        de = DOMElement(tag='div',  id='divId',  classes=["divClass1",  "divClass2"],  name="divName")
        self.assertEqual("<div id='divId' name='divName' class='divClass1 divClass2'></div>",  str(de))
    
    def test_add_tag(self):
        self.de.set_tag('html')
        self.assertEqual("<html></html>", str(self.de))
    
    def test_get_tag(self):
        self.assertEqual('div', self.div.get_tag())
    
    def test_add_id(self):
        self.div.set_id('divId')
        self.assertEqual("<div id='divId'></div>", str(self.div))
    
    def test_get_id(self):
        self.div.set_id('divId')
        self.assertEqual('divId', self.div.get_id())
    
    def test_set_class(self):
        self.div.set_class('divClass')
        self.assertEqual("<div class='divClass'></div>", str(self.div))
    
    def test_add_class(self):
        self.div.set_class('divClass1')
        self.div.add_class('divClass2')
        self.assertEqual("<div class='divClass1 divClass2'></div>",  str(self.div))
    
    def test_get_class1(self):
        self.div.set_class('divClass')
        self.assertEqual(['divClass'], self.div.get_class())
    
    def test_get_class2(self):
        self.div.set_class('divClass1')
        self.div.add_class('divClass2')
        self.assertEqual(['divClass1', 'divClass2'],  self.div.get_class())
    
    def test_set_name(self):
        self.div.set_name('divName')
        self.assertEqual("<div name='divName'></div>", str(self.div))
    
    def test_get_name(self):
        self.div.set_name('divName')
        self.assertEqual('divName', self.div.get_name())

if __name__ == "__main__":
    unittest.main()
