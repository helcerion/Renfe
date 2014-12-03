# ------------------------------------------------------------------------------
# Name:        dom_element
#
# Author:      Albert
# ------------------------------------------------------------------------------
#!/usr/bin/env python


class DOMElement:

    def __init__(self,  **kwargs):
        self._tag = ""  # tag name
        self._attr = {}  # dict of attr
        self._children = []  # list of children
        self._listIds = {}  # dict of id from tree
        self._listClasses = {}  # dict of list from classes of tree
        self._listNames = {}  # dict of list from names of tree
        self._listTags = {}  # dict of list from tags of tree
        self._text = None
        self._parent = None
        self.set_attrs(kwargs)
    
    def __str__(self):
        result = "<" + (self._tag + " " + ' '.join([k+"='"+self._attr[k]+"'" for k in self._attr.keys()])).strip() + ">"
        if self._text is not None:
            result = result + self._text
        for child in self._children:
            result += str(child)
        result = result + "</" + self._tag+">"
        return result
    
    def set_id(self,  element_id):
        self._attr['id'] = element_id
        self.add_list_ids({element_id: self})
    
    def get_id(self):
        return self._attr['id']
    
    def set_class(self,  classe):
        self._attr['class'] = classe
        self.add_list_classes({classe: self})
    
    def get_class(self):
        return self._attr['class'].split()
    
    def add_class(self,  classe):
        if 'class' in self._attr:
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
        self.add_list_tags({tag: self})
    
    def get_tag(self):
        return self._tag
    
    def set_attrs(self, attrs):
        if 'tag' in attrs:
            self._tag = attrs.pop('tag')
            self._listTags[self._tag] = [self]
        if 'id' in attrs:
            self._attr['id'] = attrs.pop('id')
            self._listIds[self._attr['id']] = self
        if 'classes' in attrs:
            self._attr['class'] = ' '.join(attrs['classes'])
            for cls in attrs.pop('classes'):
                self._listClasses[cls] = [self]
        if 'class' in attrs:
            self._attr['class'] = ' '.join(attrs['class'].split())
            for cls in (attrs.pop('class')).split():
                self._listClasses[cls] = [self]
        if 'name' in attrs:
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
    
    def get_element_by_id(self, element_id):
        return self._listIds.get(element_id)
    
    def add_list_classes(self,  classes):
        for k in classes.keys():
            if k in self._listClasses:
                aux = self._listClasses[k]
                aux.append(classes[k])
                self._listClasses[k] = list(set(aux))
            else:
                self._listClasses[k] = [classes[k]]
    
    def get_elements_by_class(self, classe):
        return self._listClasses.get(classe, [])
    
    def add_list_names(self,  names):
        for k in names.keys():
            if k in self._listNames:
                aux = self._listNames[k]
                aux.append(names[k])
                self._listNames[k] = list(set(aux))
            else:
                self._listNames[k] = [names[k]]
    
    def get_elements_by_name(self, name):
        return self._listNames.get(name)
    
    def add_list_tags(self, tags):
        for k in tags.keys():
            if k in self._listTags:
                aux = self._listTags[k]
                aux.append(tags[k])
                self._listTags[k] = list(set(aux))
            else:
                self._listTags[k] = [tags[k]]
    
    def get_elements_by_tag(self,  tag):
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
    
    def bubble_classes(self, list_classes):
        for k in list_classes.keys():
            for classe in list_classes[k]:
                self._parent.add_list_classes({k: classe})
        if self._parent.get_parent() is not None:
            self._parent.bubble_classes(list_classes)
    
    def bubble_ids(self, list_ids):
        for k in list_ids.keys():
            self._parent.add_list_ids({k: list_ids[k]})
        if self._parent.get_parent() is not None:
            self._parent.bubble_ids(list_ids)
    
    def bubble_names(self, list_names):
        for k in list_names.keys():
            for name in list_names[k]:
                self._parent.add_list_names({k: name})
        if self._parent.get_parent() is not None:
            self._parent.bubble_names(list_names)
    
    def bubble_tags(self, list_tags):
        for k in list_tags.keys():
            for tag in list_tags[k]:
                self._parent.add_list_tags({k: tag})
        if self._parent.get_parent() is not None:
            self._parent.bubble_tags(list_tags)
