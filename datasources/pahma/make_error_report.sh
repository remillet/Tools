echo "Solr Refesh Errors `date`"
echo
wc -l counts*.csv
echo
echo "Unspecified data problems, probably stray newlines or tabs"
echo
echo Public core
echo
grep error counts.public.csv | cut -f2
echo
echo Internal core
echo
grep error counts.internal.csv | cut -f2
echo
echo "Errors in Coordinates"
echo
cut -f3 counts.latlong_errors.csv
echo
