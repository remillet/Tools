#!/usr/bin/env bash

CREDS="xxx@ucjeps.cspace.berkeley.edu:xxx"
PAGESIZE=2000
STILLTODO=1


function extract()
{
   cat <<HERE > new1.xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns2:abstract-common-list xmlns:ns2="http://collectionspace.org/services/jaxb">
</ns2:abstract-common-list>
HERE

   while [ $STILLTODO -ne 0 ]; do
       PAGENUM=0
       curl -u "${CREDS}" -o tmp.xml "https://ucjeps.cspace.berkeley.edu/cspace-services/$1/items?pgSz=${PAGESIZE}&pgNum=${PAGENUM}&wf_deleted=false"


       if [ `grep "<itemsInPage>0</itemsInPage>" tmp.xml` ]
       then
            break
       fi

       python combinexml.py new1.xml tmp.xml > new2.xml
       mv new2.xml new1.xml

       PAGENUM=`expr $PAGENUM + 1`
       echo "Page ${PAGENUM}"

    done

   xmllint --format new2.xml > ~/extracts/ucjeps-authorities/$2.xml
   rm tmp.xml new1.xml new2.xml
}



extract orgauthorities/225e44ef-7f3d-4660-a4d6 nomenclature
extract orgauthorities/751023ec-d953-45f9-a0a8 determination
extract orgauthorities/a71f4ab6-221a-4202-bf75 institution
extract orgauthorities/dcba2506-20fd-438b-9adc typeassertion
# extract orgauthorities/f53284f1-0462-4326-92e7 organizationtest
extract orgauthorities/6d89bda7-867a-4b97-b22f organization
extract personauthorities/492326d1-efb1-4d2b-96d9 person
# extract taxonomyauthority/87036424-e55f-4e39-bd12 taxonomyauthority
rm -f  ~/extracts/ucjeps-authorities/authorities.tgz
tar -czf  ~/extracts/ucjeps-authorities/authorities.tgz ~/extracts/ucjeps-authorities
