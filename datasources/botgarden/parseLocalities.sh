#
# hack of a utility script to analyze Locality field
# nb: this is already implemented in the solrETL scripts...
#
cut -f23 -d$'\t' 4solr.botgarden.public.csv | sort | uniq -c | sort -rn | perl -pe 's/^ *(\d+) /\1\t/' > localities.csv
perl -ne 'chomp; $x = $_ ; s/^.*?\t//;s/, +/,/g;s/Geographic range: +//; @y=split ",",",,,,," . $_; print $x; print join "\t",@y[$#y - 5 .. $#y]; print "\n";' localities.csv > ex.csv
