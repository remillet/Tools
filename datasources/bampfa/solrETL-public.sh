#!/bin/bash -x
date
cd /home/app_solr/solrdatasources/bampfa
##############################################################################
# move the current set of extracts to temp (thereby saving the previous run, just in case)
# note that in the case where there are several nightly scripts, e.g. public and public,
# the one to run first will "clear out" the previous night's data.
# NB: at the moment BAMPFA has only an public portal.
# since we don't know which order these might run in, I'm leaving the mv commands in both
# nb: the jobs in general can't overlap as the have some files in common and would step
# on each other
##############################################################################
mv 4solr.*.csv.gz /tmp
##############################################################################
# while most of this script is already tenant specific, many of the specific commands
# are shared between the different scripts; having them be as similar as possible
# eases maintainance. ergo, the TENANT parameter
##############################################################################
TENANT=$1
SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
USERNAME="reporter_$TENANT"
DATABASE="${TENANT}_domain_${TENANT}"
CONNECTSTRING="host=$SERVER dbname=$DATABASE"
##############################################################################
# extract metadata and media info from CSpace
##############################################################################
# note this query included current location and current crate, which are
# removed later. The values are needed, however, to calculate viewing status
time psql -R"@@" -F $'\t' -A -U $USERNAME -d "$CONNECTSTRING"  -f metadata_public.sql -o d1.csv
# some fix up required, alas: data from cspace is dirty: contain csv delimiters, newlines, etc. that's why we used @@ as temporary record separator
time perl -pe 's/[\r\n]/ /g;s/\@\@/\n/g' d1.csv > d3.csv 
##############################################################################
# check cell counts
##############################################################################
time python evaluate.py d3.csv d4.csv > counts.public.errors.csv
time psql -R"@@" -F $'\t' -A -U $USERNAME -d "$CONNECTSTRING" -f media_public.sql -o m1.csv
time perl -pe 's/[\r\n]/ /g;s/\@\@/\n/g' m1.csv > media.csv 
time psql -R"@@" -F $'\t' -A -U $USERNAME -d "$CONNECTSTRING" -f blobs.sql -o b1.csv
time perl -pe 's/[\r\n]/ /g;s/\@\@/\n/g' b1.csv > blobs.csv
# Compute the "view status" of each object
time perl addStatus.pl public 37 38 < d4.csv > metadata.csv
# make the header
head -1 metadata.csv > header4Solr.csv
# add the blob field name to the header (the header already ends with a tab); rewrite objectcsid_s to id (for solr id...)
perl -i -pe 's/\r//;s/\t/_s\t/g;s/objectcsid_s/id/;s/$/_s\tblob_ss/;s/_ss_s/_ss/;' header4Solr.csv
# add the blobcsids to the rest of the data
time perl mergeObjectsAndMedia.pl media.csv metadata.csv > d6.csv
# we want to use our "special" solr-friendly header.
tail -n +2 d6.csv > d7.csv
cat header4Solr.csv d7.csv > d8.csv
##############################################################################
# compute _i values for _dt values (to support BL date range searching)
##############################################################################
time python computeTimeIntegers.py d8.csv 4solr.$TENANT.public.csv
wc -l *.csv
# clear out the existing data
curl -S -s "http://localhost:8983/solr/${TENANT}-public/update" --data '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'
curl -S -s "http://localhost:8983/solr/${TENANT}-public/update" --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'
# note: current location, current crate, appraised values have all been redacted
# in the sql queries themselves.
# some values were needed for computing the status field (i.e. "on view")
# TODO however we could also skip them in the Solr load as well...
time curl -X POST -S -s "http://localhost:8983/solr/${TENANT}-public/update/csv?commit=true&header=true&trim=true&separator=%09&f.grouptitle_ss.split=true&f.grouptitle_ss.separator=;&f.othernumbers_ss.split=true&f.othernumbers_ss.separator=;&f.blob_ss.split=true&f.blob_ss.separator=,&encapsulator=\\" -T 4solr.$TENANT.public.csv -H 'Content-type:text/plain; charset=utf-8' &
##############################################################################
# count the types and tokens in the final file, check cell counts
##############################################################################
time python evaluate.py 4solr.$TENANT.public.csv /dev/null > counts.public.csv &
# get rid of intermediate files
rm d?.csv m?.csv b?.csv media.csv metadata.csv &
cut -f43 4solr.${TENANT}.public.csv | grep -v 'blob_ss' |perl -pe 's/\r//' |  grep . | wc -l > counts.public.blobs.csv
cut -f43 4solr.${TENANT}.public.csv | perl -pe 's/\r//;s/,/\n/g;s/\|/\n/g;' | grep -v 'blob_ss' | grep . | wc -l >> counts.public.blobs.csv
cp counts.public.blobs.csv /tmp/$TENANT.counts.public.csv
cat counts.public.blobs.csv
wait
cp counts.public.csv /tmp/$TENANT.counts.public.csv
# zip up .csvs, save a bit of space on backups
gzip -f *.csv
date
