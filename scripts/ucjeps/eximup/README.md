### Scripts and Methods to prepare DWC files (e.g. Symbiota) for upload to CSpace

```
# prep for various "recoding" processes (further below)
# scp cspace-prod.cspace.berkeley.edu:/tmp/authorities.tgz .
tar xvzf authorities.tgz 
mv home/app_webapps/extracts/ucjeps-authorities/* .
rm -rf home/
scp cspace-prod.cspace.berkeley.edu:/tmp/taxon_auth.txt.gz .
scp cspace-prod.cspace.berkeley.edu:/tmp/unverified_auth.txt.gz .
scp cspace-prod.cspace.berkeley.edu:/tmp/major_group.txt.gz .
python extractFromAuthority.py organization.xml organization.csv > duplicates.txt

./makeSubsTables.sh 
less occurrences_Jul102018.txt

python checkcsv.py july.csv checked_file.csv > micro_algae_stats.csv
expand -30 micro_algae_stats.csv 
perl recodeColumns.pl taxon-2cols.csv /dev/null july.csv part.1.csv 15 999

head -3 test50.csv > test3.csv
python DWC2CSpace.py test3.csv ucjeps_DWC2Cspace_Dev.cfg DWC2CSpace.csv collectionobject.xml output.txt

# $ python loadAuthority.py
# loadAuthority.py <csv input file> <config file> <mapping file> <template> <output file>
nohup python loadAuthority.py algaeNON1-collectors_to_add.txt ucjeps_DWC2Cspace_Dev.cfg orgauthorities/6d89bda7-867a-4b97-b22f ucjeps.orgauthorities.xml algaeNON1-collectors_to_add.log &

cut -f5 -d" " algaeNON1-collectors_to_add.log > csids.txt
vi csids.txt

# if you haven't already, do the following steps to set some environment vars needed by the scripts 
# cp set-config-ucjeps-dev.sh.example set-config-ucjeps-dev.sh
# add login and password
# vi set-config-ucjeps-dev.sh
# if you haven't already set the environment vars this session, do so now
# source set-config-ucjeps-dev.sh

# here's how to delete the authority records you added in the step above:
nohup ./delete-multiple.sh orgauthorities/6d89bda7-867a-4b97-b22f/items csids.txt &

```
