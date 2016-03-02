#!/usr/bin/env python
# -*- coding: utf-8 -*-



import xml.etree.cElementTree as ET


#https://discussions.udacity.com/t/project-creating-example-osm-file/19191

OSM_FILE = "../chicago.osm"
SAMPLE_FILE = "../chicago_small.osm"


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context) # ignore the first tag: <osm>
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            # this is a generator so 'yield' returns the whole content (i.e. children, attributes, text, etc.). 
            #'return' won't work the same. http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python            
            yield elem
            # clear the content from memory (I think)            
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every 30th top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % 30 == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')