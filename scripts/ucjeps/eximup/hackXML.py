#
#
# 1. read and parse the UCJEPS FIMS CSpace IMPORT XML File.
# 2. eliminate the <identDateGroup> element
# 3. write out the result
#
# takes 1 argument:
#
# UCJEPS FIMS CSpace IMPORT XML File
# (output goes to STDOUT)
#
# to run:
#
# python hackXML.py c4.xml > noidentgroup.xml
#

import xml.etree.ElementTree as ET
import sys, csv, codecs, re

reload(sys)
sys.setdefaultencoding('utf-8')


def extractTag(xml, tag):
    element = xml.find('.//%s' % tag)
    return element.text

try:
    FIMS_CSPACE_XML = ET.parse(sys.argv[1])
    root = FIMS_CSPACE_XML.getroot()

    for parent in FIMS_CSPACE_XML.findall('.//taxonomicIdentGroup'):
        for element in parent.findall('identDateGroup'):
            #print element
            parent.remove(element)


except:
    raise
    print sys.stderr, 'could not read or parse FIMS config XML file: %s' % sys.argv[1]
    exit(0)

#print '%s identDateGroups deleted.' % len(identDateGroups)
print ET.tostring(root)
