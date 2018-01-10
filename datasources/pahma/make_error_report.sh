echo "Solr Refresh, Field Counts and Errors `date`"
echo
for F in `ls counts.*.csv`
do
  ERRORS=`grep errors $F`
  if [ "$ERRORS" == "" ]; then
    echo "$F: no errors detected."
  else
    echo "$F: $ERRORS"
  fi
done
echo
