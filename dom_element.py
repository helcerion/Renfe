#-------------------------------------------------------------------------------
# Name:        dom_element
#
# Author:      Albert
#-------------------------------------------------------------------------------
#!/usr/bin/env python

class DOMElement:

    def __init__(self,  **kwargs):
        self._tag = "" # tag name
        self._attr = {} # dict of attr
        self._children = [] # list of children
        self._listIds = {} # dict of id from tree
        self._listClasses = {} # dict of list from classes of tree
        self._listNames = {} # dict of list from names of tree
        self._listTags = {} # dict of list from tags of tree
        self._text = None
        self._parent = None
        self.set_attrs(kwargs)
    
    def __str__(self):
        result = "<" + (self._tag + " " + ' '.join([k+"='"+self._attr[k]+"'" for k in self._attr.keys()])).strip() + ">"
        if self._text is not None:
            result = result + self._text
        for child in self._children:
            result = result + str(child)
        result = result +"</"+self._tag+">"
        return result
    
    def set_id(self,  id):
        self._attr['id'] = id
        self.add_list_ids({id: self})
    
    def get_id(self):
        return self._attr['id']
    
    def set_class(self,  classe):
        self._attr['class'] = classe
        self.add_list_classes({classe: self})
    
    def get_class(self):
        return self._attr['class'].split()
    
    def add_class(self,  classe):
        if self._attr.has_key('class'):
            aux = self._attr['class'].split()
            aux.append(classe)
            self._attr['class'] = ' '.join(aux)
        else:
            self._attr['class'] = classe
        self.add_list_classes({classe: self})
    
    def set_name(self,  name):
        self._attr['name'] = name
        self.add_list_names({name: self})
    
    def get_name(self):
        return self._attr['name']
    
    def set_tag(self, tag):
        self._tag = tag
        self.add_list_tags({tag:self})
    
    def get_tag(self):
        return self._tag
    
    def set_attrs(self, attrs):
        if attrs.has_key('tag'):
            self._tag = attrs.pop('tag')
            self._listTags[self._tag] = [self]
        if attrs.has_key('id'):
            self._attr['id'] = attrs.pop('id')
            self._listIds[self._attr['id']] = self
        if attrs.has_key('classes'):
            self._attr['class'] = ' '.join(attrs['classes'])
            for cls in attrs.pop('classes'):
                self._listClasses[cls] = [self]
        if attrs.has_key('class'):
            self._attr['class'] = ' '.join(attrs['class'].split())
            for cls in (attrs.pop('class')).split():
                self._listClasses[cls] = [self]
        if attrs.has_key('name'):
            self._attr['name'] = attrs.pop('name')
            self._listNames[self._attr['name']] = [self]
        for attr in attrs.keys():
            self._attr[attr] = attrs[attr]
    
    def get_attrs(self):
        return self._attr
    
    def get_attr(self, attr):
        return self._attr.get(attr)
    
    def add_list_ids(self,  ids):
        for k in ids.keys():
            self._listIds[k] = ids[k]
    
    def getElementById(self, id):
        return self._listIds.get(id)
    
    def add_list_classes(self,  classes):
        for k in classes.keys():
            if self._listClasses.has_key(k):
                aux = self._listClasses[k]
                aux.append(classes[k])
                self._listClasses[k] = list(set(aux))
            else:
                self._listClasses[k] = [classes[k]]
    
    def getElementsByClass(self, classe):
        return self._listClasses.get(classe, [])
    
    def add_list_names(self,  names):
        for k in names.keys():
            if self._listNames.has_key(k):
                aux = self._listNames[k]
                aux.append(names[k])
                self._listNames[k] = list(set(aux))
            else:
                self._listNames[k] = [names[k]]
    
    def getElementsByName(self, name):
        return self._listNames.get(name)
    
    def add_list_tags(self, tags):
        for k in tags.keys():
            if self._listTags.has_key(k):
                aux = self._listTags[k]
                aux.append(tags[k])
                self._listTags[k] = list(set(aux))
            else:
                self._listTags[k] = [tags[k]]
    
    def getElementsByTag(self,  tag):
        return self._listTags.get(tag, [])
    
    def set_text(self, text):
        self._text = text
    
    def get_text(self):
        return self._text
    
    def add_children(self,  children):
        self._children.append(children)
        children.set_parent(self)
    
    def get_children(self):
        return self._children
    
    def set_parent(self, parent):
        self._parent = parent
        self.bubble_classes(self._listClasses)
        self.bubble_ids(self._listIds)
        self.bubble_names(self._listNames)
        self.bubble_tags(self._listTags)

    def get_parent(self):
        return self._parent
    
    def bubble_classes(self, listClasses):
        for k in listClasses.keys():
            for classe in listClasses[k]:
                self._parent.add_list_classes({k:classe})
        if self._parent.get_parent() is not None:
            self._parent.bubble_classes(listClasses)
    
    def bubble_ids(self, listIds):
        for k in listIds.keys():
            self._parent.add_list_ids({k:listIds[k]})
        if self._parent.get_parent() is not None:
            self._parent.bubble_ids(listIds)
    
    def bubble_names(self, listNames):
        for k in listNames.keys():
            for name in listNames[k]:
                self._parent.add_list_names({k:name})
        if self._parent.get_parent() is not None:
            self._parent.bubble_names(listNames)
    
    def bubble_tags(self, listTags):
        for k in listTags.keys():
            for tag in listTags[k]:
                self._parent.add_list_tags({k:tag})
        if self._parent.get_parent() is not None:
            self._parent.bubble_tags(listTags)
