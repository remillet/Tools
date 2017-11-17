import sys, csv, codecs

reload(sys)
sys.setdefaultencoding('utf-8')

def get_date_rows(row):
    date_rows = []
    for i,r in enumerate(row):
        if "_dt" in r:
            row.append(r.replace('_dt', '_i'))
            date_rows.append(i)
    return date_rows

def get_year(date_value):
    return date_value[0:4]

file_with_integer_times = csv.writer(codecs.open(sys.argv[2], 'w', "utf-8"), delimiter='\t')
try:
    for i,row in enumerate(csv.reader(codecs.open(sys.argv[1], 'r', "utf-8"), delimiter='\t')):
        if i == 0:
            date_rows = get_date_rows(row)
        else:
            for d in date_rows:
                row.append(get_year(row[d]))
        file_with_integer_times.writerow(row)
except:
    raise
    print 'couldnt'
    exit()


