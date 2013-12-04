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
        if kwargs.has_key('tag'):
            self._tag = kwargs['tag']
            self._listTags[self._tag] = [self]
        if kwargs.has_key('id'):
            self._attr['id'] = kwargs['id']
            self._listIds[self._attr['id']] = self
        if kwargs.has_key('classes'):
            self._attr['class'] = ' '.join(kwargs['classes'])
            for cls in kwargs['classes']:
                self._listClasses[cls] = [self]
        if kwargs.has_key('name'):
            self._attr['name'] = kwargs['name']
            self._listNames[self._attr['name']] = [self]
    
    def __str__(self):
        return "<" + (self._tag + " " + ' '.join([k+"='"+self._attr[k]+"'" for k in self._attr.keys()])).strip() + ">"+''.join(self._children)+"</"+self._tag+">"
    
    def set_id(self,  id):
        self._attr['id'] = id
        self._listIds[id] = self
    
    def get_id(self):
        return self._attr['id']
    
    def set_class(self,  classe):
        self._attr['class'] = classe
        if self._listClasses.has_key(classe):
            self._listClasses[classe].append(self)
        else:
            self._listClasses[classe] = [self]
    
    def get_class(self):
        return self._attr['class'].split()
    
    def add_class(self,  classe):
        if self._attr.has_key('class'):
            aux = self._attr['class'].split()
            aux.append(classe)
            self._attr['class'] = ' '.join(aux)
        else:
            self._attr['class'] = classe
        if self._listClasses.has_key(classe):
            self._listClasses[classe].append(self)
        else:
            self._listClasses[classe] = [self]
    
    def set_name(self,  name):
        self._attr['name'] = name
        if self._listNames.has_key(name):
            self._listNames[name].append(self)
        else:
            self._listNames[name] = [self]
    
    def get_name(self):
        return self._attr['name']
    
    def set_tag(self, tag):
        self._tag = tag
    
    def get_tag(self):
        return self._tag
    
    def add_list_ids(self,  ids):
        for k in ids.keys():
            self._listIds[k] = ids[k]
    
    def getElementById(self, id):
        return self._listIds[id]
    
    def add_list_classes(self,  classes):
        for k in classes.keys():
            if self._listClasses.has_key(k):
                self._listClasses[k].append(classes[k])
            else:
                self._listClasses[k] = [classes[k]]
    
    def getElementsByClass(self, classe):
        return self._listClasses[classe]
    
    def add_list_names(self,  names):
        for k in names.keys():
            if self._listNames.has_key(k):
                self._listNames[k].append(names[k])
            else:
                self._listNames[k] = [names[k]]
    
    def getElementsByName(self, name):
        return self._listNames[name]
    
    def add_list_tags(self, tags):
        for k in tags.keys():
            if self._listTags.has_key(k):
                self._listTags[k].append(tags[k])
            else:
                self._listTags[k] = [tags[k]]
    
    def getElementsByTag(self,  tag):
        return self._listTags[tag]
    
    def add_children(self,  children):
        pass
    
    def get_children(self):
        return self._children
