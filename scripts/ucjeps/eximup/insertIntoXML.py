#
#
# 1. read and parse the UCJEPS FIMS configuration file.
# 2. read a csv file of refnames to be added to the file
# 3. check for duplicates, add refnames and display names to the appropriate section.
#
# takes 3 arguments:
#
# UCJEPS FIMS configuration file
# a delimited file (tabs, no encapsulation)
# an integer for the column containing the refnames, starting from column 0
#
#
# e.g. to make a nicely formatted new_ucjeps_fims.xml with revised Collector names in the 4th column of
#      a csv file created by extractFromAuthority.py...
#
# python insertIntoXML.py ucjeps_fims.xml organization.csv 3 | xmllint --format - > new_ucjeps_fims.xml
#
import xml.etree.ElementTree as ET
import sys, csv, codecs, re

reload(sys)
sys.setdefaultencoding('utf-8')


def extractTag(xml, tag):
    element = xml.find('.//%s' % tag)
    return element.text


def find_alias(refname):
    # only the following authorities are currently handled
    # 'Label_Header' urn:cspace:ucjeps.cspace.berkeley.edu:conceptauthorities:name(concept):item:name
    # and ... nb, label footers and headers cannot be distinguished this way, only label header are handled
    # 'Label_Footer'  urn:cspace:ucjeps.cspace.berkeley.edu:conceptauthorities:name(concept):item:name
    # 'Collector'        urn:cspace:ucjeps.cspace.berkeley.edu:orgauthorities:name(organization) :item:name
    # 'DeterminedBy' urn:cspace:ucjeps.cspace.berkeley.edu:orgauthorities:name(determination):item:name
    # 'ScientificName' urn:cspace:ucjeps.cspace.berkeley.edu:taxonomyauthority:name(taxon):item:name
    if 'conceptauthorities' in refname and 'concept' in refname:
        return 'Label_Header'
    elif 'conceptauthorities' in refname and 'concept' in refname:
        return 'Label_Footer'
    elif 'orgauthorities' in refname and 'organization' in refname:
        return 'Collector'
    elif 'orgauthorities' in refname and 'determination' in refname:
        return 'DeterminedBy'
    elif 'taxonomyauthority' in refname and 'taxon' in refname:
        return 'ScientificName'


try:
    FIMS_XML = ET.parse(sys.argv[1])
    root = FIMS_XML.getroot()
    lists = FIMS_XML.findall('.//list')
except:
    print sys.stderr, 'could not read or parse FIMS config XML file'
    exit(0)

try:
    column = int(sys.argv[3])
except:
    print sys.stderr, 'looking for refName in 1st column (0)'
    column = 0

try:
    refNamesRows = csv.reader(codecs.open(sys.argv[2], 'r', "utf-8"), delimiter='\t')
    refNames = [r[column] for r in refNamesRows]
except:
    print sys.stderr, 'could not read or parse input file for refNames'
    exit(0)

numberoflists = len(lists)

displayNames = [ d.text for d in root.findall(".//field")]

for r in refNames:
    # e.g. <field uri="urn:cspace:ucjeps.cspace.berkeley.edu:orgauthorities:name(organization):item:name(3333)"><![CDATA[Katharine Brandegee]]></field>
    refName_parsed = re.match(r"^(.*name.*?\))\'(.*)\'", r)
    refName = refName_parsed.group(1)
    displayName = refName_parsed.group(2)
    # check for duplicates
    if not displayName in displayNames:
        refNameElement = ET.Element('field')
        refNameElement.text = displayName
        refNameElement.set('uri', refName)
        # print ET.tostring(refNameElement)
        alias = find_alias(r)
        aliasElement = root.find(".//*[@alias='%s']" % alias)
        aliasElement.append(refNameElement)
    else:
        print sys.stderr, "refName not found %s" % r

print ET.tostring(root)
