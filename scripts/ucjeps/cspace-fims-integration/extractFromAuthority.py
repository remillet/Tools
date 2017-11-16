import xml.etree.ElementTree as ET
import sys, csv, codecs

reload(sys)
sys.setdefaultencoding('utf-8')

def extractTag(xml, tag):
    element = xml.find('.//%s' % tag)
    return element.text

xData = []
try:
    cspaceXML = ET.parse(sys.argv[1])
    root = cspaceXML.getroot()
    items = cspaceXML.findall('.//list-item')
    for i in items:
        csid = i.find('.//csid')
        csid = csid.text
        termDisplayName = extractTag(i, 'termDisplayName')
        refName = extractTag(i, 'refName')
        updated_at = extractTag(i, 'updatedAt')
        xData.append([csid, termDisplayName,refName,updated_at])
except:
    for row in csv.reader(codecs.open(sys.argv[1], 'r', "utf-8"), delimiter='\t'):
        # csid   displayname     refname noauthorname    majorgroup
        xData.append([row[0], row[1], row[2], 'nothing'])


cspaceCSV = csv.writer(codecs.open(sys.argv[2], 'w', "utf-8"), delimiter='\t')
entities = {}

numberofitems = len(xData)
# if numberofitems > numberWanted:
#    items = items[:numberWanted]

if len(sys.argv) >= 4:
    file_of_names2check = csv.reader(codecs.open(sys.argv[3], 'r', "utf-8"), delimiter='\t')
    names2check = [line[0].strip() for line in file_of_names2check]
    check_names = True
else:
    check_names = False

for sequence_number,i in enumerate(xData):
    [ csid,termDisplayName,refName,updated_at ] = i
    # if we were given a specific list of names, only write those ones out
    if check_names:
        if not termDisplayName in names2check:
            continue
    else:
        pass

    cspaceCSV.writerow([sequence_number, csid, termDisplayName, refName, updated_at])
