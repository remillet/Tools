import xml.etree.ElementTree as et
import sys

with open(sys.argv[1], 'r') as f:
    r = et.parse(f)
    documents = r.findall('.//document')
    for doc in documents:
        elem = doc.findall('.//{http://collectionspace.org/collectionspace_core/}collectionspace_core')
        for e in elem:
            doc.remove(e)
        elem = doc.findall('.//{http://collectionspace.org/services/authorization}account_permission')
        for e in elem:
            doc.remove(e)
        elem = doc.findall('.//{http://collectionspace.org/services/taxon/local/ucjeps}taxon_ucjeps')
        for e in elem:
            doc.remove(e)
        elem = doc.findall('.//{http://collectionspace.org/services/taxon/domain/naturalhistory}taxon_naturalhistory')
        for e in elem:
            e.tag = '{http://collectionspace.org/services/taxon/local/herbarium}taxon_herbarium'
    r.write(sys.stdout)
