import sys, csv
from unicode_hack import UnicodeReader, UnicodeWriter
from fix_fields import fix_materials, fix_name

reload(sys)
sys.setdefaultencoding('utf-8')

delim = '\t'

object_name_column = 10
object_materials_column = 17

def get_date_rows(row):
    date_rows = []
    int_year_names = []
    for i,r in enumerate(row):
        if "_dt" in r:
            row.append(r.replace('_dt', '_i'))
            int_year_name = r.replace('_dts', '_i').replace('_dt', '_i')
            int_year_names.append(int_year_name)
            date_rows.append(i)
    return date_rows, int_year_names


def get_year(date_value):
    return date_value[0:4]


def compare_years(years, int_year_names, musno):
    new_years = []
    for year in int_year_names:
        if years[year] < '1595' and years[year.replace('begin','end')] != '':
            print 'replaced %s (%s) with %s (%s) for %s' % (years[year], year, years[year.replace('begin','end')], year.replace('begin','end'), musno)
            years[year] = years[year.replace('begin','end')]
        new_years.append(years[year])
    return new_years


with open(sys.argv[2], 'wb') as f2:
    file_with_integer_times = UnicodeWriter(f2, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
    with open(sys.argv[1], 'r') as f1:
        reader = UnicodeReader(f1, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
        try:
            for i,row in enumerate(reader):
                row[object_materials_column] = fix_materials(row[object_materials_column])
                row[object_name_column] = fix_name(row[object_name_column])
                if i == 0:
                    date_rows, int_year_names  = get_date_rows(row)
                else:
                    years = {}
                    for j, d in enumerate(date_rows):
                        years[int_year_names[j]] = get_year(row[d])
                    new_years = compare_years(years, int_year_names, row[3])
                    row += new_years
                file_with_integer_times.writerow(row)
        except:
            # really someday we should do something better than just die here...
            raise
            print 'couldnt'
            exit()
        
        
