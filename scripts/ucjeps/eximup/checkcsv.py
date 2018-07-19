#
# Count types and tokens in a .csv file (argument 1) and
# check that all the rows have the same number of cells as the header
#
# e.g.
# python checkcsv.py 4solr.pahma.public.csv checked.csv > counts.csv
# head -4 counts.csv | expand -20
#
# id                  748756              748756
# objtype_s           8                   736597
# objcount_s          911                 737182
# objcountnote_s      1550                58810
#

import sys, csv, collections
# for python 2.6 :-(
from Counter import Counter


from unicode_hack import UnicodeReader, UnicodeWriter

delim = "\t"

types = {}
errors = 0

# keep these lines around for when we start to use python3
# with open(sys.argv[2], 'w', encoding='utf-8') as f2:
#    writer = csv.writer(f2, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
#    with open(sys.argv[1], 'r', encoding='utf-8') as f1:
#        reader = csv.reader(f1, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))

if len(sys.argv) != 3:
    print '\ninvoke as follows:'
    print '%s input.csv report.csv\n' % sys.argv[0]
    sys.exit(1)

try:
    writer = UnicodeWriter(open(sys.argv[2], 'w'), delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
except:
    print "could not open output file for write %s" % sys.argv[2]
    sys.exit(1)

try:
    reader = UnicodeReader(open(sys.argv[1], 'r'), delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
except:
    print "could not open input file for read %s" % sys.argv[1]
    sys.exit(1)

for lineno, row in enumerate(reader):
    if lineno == 0:
        header = row
        writer.writerow(row)
        for col in header:
            types[col] = Counter()
        column_count = len(header)
    else:
        if len(row) != column_count:
            print "%s%s%s" % ('error', delim, delim.join(row).encode('utf-8'))
            errors += 1
            continue
        for i, cell in enumerate(row):
            if cell != '':
                types[header[i]][cell] += 1
        writer.writerow(row)

if errors > 0:
    print
    print "%s errors seen (i.e. data row and header row w different counts.)" % errors
    print

print "%s\t%s\t%s" % ('column', 'types', 'tokens')
for key in header:
    print "%s\t%s\t%s" % (key, len(types[key]), sum(types[key].values()))
    try:
        writer = UnicodeWriter(open('%s.values.csv' % key, 'w'), delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
    except:
        print "could not write to '%s.values.csv'" % key
        sys.exit(1)
    for token in sorted(types[key]):
        writer.writerow([token, str(types[key][token])])
