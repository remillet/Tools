#!/usr/bin/env bash

CREDS="xxx@ucjeps.cspace.berkeley.edu:xxx"
 
function extract()
{
   curl -u "${CREDS}" -o tmp.xml "https://ucjeps.cspace.berkeley.edu/cspace-services/$1/items?pgSz=10000"
   xmllint --format tmp.xml > $2.xml
   rm tmp.xml
}

extract orgauthorities/225e44ef-7f3d-4660-a4d6 nomenclature
extract orgauthorities/751023ec-d953-45f9-a0a8 determination
extract orgauthorities/a71f4ab6-221a-4202-bf75 institution
extract orgauthorities/dcba2506-20fd-438b-9adc typeassertion
# extract orgauthorities/f53284f1-0462-4326-92e7 organizationtest
extract orgauthorities/6d89bda7-867a-4b97-b22f organization
extract personauthorities/492326d1-efb1-4d2b-96d9 person
# extract taxonomyauthority/87036424-e55f-4e39-bd12 taxonomyauthority
