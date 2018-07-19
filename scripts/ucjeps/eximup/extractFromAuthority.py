import xml.etree.ElementTree as ET
import sys, csv, codecs

reload(sys)
sys.setdefaultencoding('utf-8')


if len(sys.argv) < 3:
    print ""
    print "reads a CSpace authority XML file and outputs CSIDs, displayNames, and refNames as a .csv file"
    print ""
    print "if a 3rd argument is present, it is assumed to be a list of displaynames to be used to filter the output"
    print ""
    print "if duplicate displaynames are seen this are output to stdout"
    print ""
    print "usage: python %s <authorityfile.xml> <outputfile.csv> <optionallistofname.txt > listofdups.txt" % sys.argv[0]
    print ""
    print "e.g:   python %s organization.xml organization.csv orgnames_to_extract.txt > listofdups.txt" % sys.argv[0]
    print ""
    print "columns are: sequence numbder, csid, displayname, refname"
    print ""
    exit(1)



def extract_tag(xml, tag):
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
        try:
            termDisplayName = extract_tag(i, 'termDisplayName')
            refName = extract_tag(i, 'refName')
            updated_at = extract_tag(i, 'updatedAt')
        except:
            print 'could not get termDisplayName or refName or updatedAt from %s' % csid
            continue
        xData.append([csid, termDisplayName, refName, updated_at])
    del items, root, cspaceXML
except:
    raise
    for row in csv.reader(codecs.open(sys.argv[1], 'r', "utf-8"), delimiter='\t'):
        # csid   displayname     refname noauthorname    majorgroup
        xData.append([row[0], row[1], row[2], 'n.d.'])

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

name_dict = {}
for sequence_number, i in enumerate(xData):
    [csid, termDisplayName, refName, updated_at] = i
    # if we were given a specific list of names, only write those ones out
    if check_names:
        if termDisplayName not in names2check:
            continue
    else:
        pass

    if termDisplayName in name_dict:
        print '%s (%s) already seen as %s' % (termDisplayName, refName, name_dict[termDisplayName])
    else:
        name_dict[termDisplayName] = refName
    cspaceCSV.writerow([sequence_number, csid, termDisplayName, refName, updated_at])
