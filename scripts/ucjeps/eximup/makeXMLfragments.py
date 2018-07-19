import xml.etree.ElementTree as ET
import sys, csv, time
import cspace
import urllib

tree = ET.parse(sys.argv[1])
root = tree.getroot()

from constants import *

relations = ['collectionobjects2storagelocations', 'collectionobjects2people']

cspaceCSV = csv.writer(open('entities.csv', 'wb'), delimiter='\t')
entities = {}

taxon_authority_csid = '87036424-e55f-4e39-bd12'
numberWanted = 10
sequence_number = 0

cspaceTime = time.time()
connection = cspace.connection.create_connection(config, request.user)


def extractTag(xml, tag):
    element = xml.find('.//%s' % tag)
    try:
        if "urn:" in element.text:
            element_text = deURN(str(element.text))
        else:
            element_text = element.text
    except:
        element_text = ''
    return element_text


for taxon in items:
    requestURL = 'cspace-services/taxonomyauthority/%s/items?pt=%s&wf_deleted=false&pgSz=%s' % (
        taxon_authority_csid, urllib.quote_plus(taxon), numberWanted)
    (url, data, statusCode, elapsedTime) = connection.make_get_request(requestURL)
    if statusCode != 200 or data is None:
        data = '<error>error %s</error>' % statusCode
    cspaceXML = ET.fromstring(data)
    items = cspaceXML.findall('.//list-item')
    numberofitems = len(items)
    if numberofitems > numberWanted:
        items = items[:numberWanted]
    for i in items:
        sequence_number += 1
        csid = i.find('.//csid')
        csid = csid.text
        termDisplayName = extractTag(i, 'termDisplayName')
        taxonRefname = extractTag(i, 'taxon')
        (url, taxondata, statusCode, elapsedTime) = connection.make_get_request(
            'cspace-services/taxonomyauthority/%s/items/%s' % (taxon_authority_csid, csid))
        print '%s cspace-services/taxonomyauthority/%s/items/%s' % (elapsedTime, taxon_authority_csid, csid)
        taxonXML = ET.fromstring(taxondata)
        family = extractTag(taxonXML, 'family')
        major_group = extractTag(taxonXML, 'taxonMajorGroup')
        updated_at = extractTag(taxonXML, 'updatedAt')
        # termDisplayName = extract_tag(taxonXML, 'termDisplayName')
        termName = extractTag(taxonXML, 'termName')
        commonName = extractTag(taxonXML, 'commonName')
        cspaceCSV.writerow([sequence_number,csid,termDisplayName,taxonRefname,family,major_group])

