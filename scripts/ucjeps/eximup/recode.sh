
# recode collecters, determiners, and other persons
perl recodeColumns.pl taxon-2cols.csv         /dev/null $1         part.2.csv 14 999
perl recodeColumns.pl determination-2cols.csv /dev/null part.2.csv part.3.csv 21 999
perl recodeColumns.pl organization-2cols.csv  /dev/null part.3.csv part.4.csv 28 999
perl recodeColumns.pl organization-2cols.csv  /dev/null part.4.csv part.5.csv 30 999
perl recodeColumns.pl taxon-2cols.csv         /dev/null part.5.csv part.6.csv 47 999

# recode the tripartite location data
perl recodeColumns.pl country-2cols.csv       /dev/null part.6.csv part.7.csv 57 999
perl recodeColumns.pl state-2cols.csv         /dev/null part.7.csv part.8.csv 58 999
perl recodeColumns.pl county-2cols.csv        /dev/null part.8.csv part.9.csv 59 999

# recode these fields to refnames when the become available
#perl recodeColumns.pl kingdom-2cols.csv      /dev/null part.x.csv part.x.csv  9 999
#perl recodeColumns.pl phylum-2cols.csv       /dev/null part.x.csv part.x.csv 10 999
#perl recodeColumns.pl class-2cols.csv        /dev/null part.x.csv part.x.csv 11 999
#perl recodeColumns.pl order-2cols.csv        /dev/null part.x.csv part.x.csv 12 999
#perl recodeColumns.pl family-2cols.csv       /dev/null part.x.csv part.x.csv 12 999
#perl recodeColumns.pl genus-2cols.csv        /dev/null part.x.csv part.x.csv 17 999
#perl recodeColumns.pl majorgroup-2cols.csv   /dev/null part.x.csv part.x.csv xx 999

mv part.9.csv recoded.csv
