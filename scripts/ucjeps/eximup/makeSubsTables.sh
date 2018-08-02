# get the zipped files
#gunzip *.gz

# get the authorities xml files
#tar xzvf authorities.tgz 
#mv home/app_webapps/extracts/ucjeps-authorities/* .
#rm -rf home/

# get the right columns for taxon names
cut -f2,3 taxon_auth.txt > taxon_auth-2cols.csv
cut -f2,3 unverified_auth.txt > unverified_auth-2cols.csv
cat taxon_auth-2cols.csv unverified_auth-2cols.csv > taxon-2cols.csv

# extract a csv file for each authority with displayname and refname
for authority in organization person nomenclature determination institution typeassertion
do
 python extractFromAuthority.py ${authority}.xml ${authority}.csv > ${authority}.duplicates.txt
 cut -f3,4 ${authority}.csv > ${authority}-2cols.csv
done

wc -l *-2cols.csv
