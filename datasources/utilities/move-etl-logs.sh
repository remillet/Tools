#
# move logs to new location
#
# in principle, this only needed to be done once for dev and prod, so this really
# record of what was done...
#
cd
SOLRETLDIR=~/solrdatasources
# copy all the logs back, for posterity
for t in bampfa botgarden cinefiles pahma ucjeps
do
    for d in public internal propagations locations media osteology
    do
       if [[ -e ${SOLRETLDIR}/${t}/solr_extract_${d}.log ]]
       then
           cp ${SOLRETLDIR}/${t}/solr_extract_${d}.log ~/logs/${t}.solr_extract_${d}.log
       fi
    done
done
cp solrdatasources/*/*.log logs
cd logs/
mv solr_extract_BAM.log bampfa.solr_extract_BAM.log
mv solr_extract_Piction.log bampfa.solr_extract_Piction.log
mv solr_extract_propagations.log botgarden.solr_extract_propagations.log
mv solr_extract_osteology.log pahma.solr_extract_osteology.log
mv solr_extract_locations.log pahma.solr_extract_locations.log
