import sys, csv
from datetime import datetime
from unicode_hack import UnicodeReader, UnicodeWriter
from fix_fields import fix_materials, fix_name

reload(sys)
sys.setdefaultencoding('utf-8')

delim = '\t'

object_name_column = 10
object_materials_column = 17

current_year = datetime.today().strftime("%Y")

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
        candidate_replacement_year = years[year.replace('begin','end')]
        if years[year] < '1695' and candidate_replacement_year != '' and candidate_replacement_year <= current_year:
            print 'replaced %s (%s) with %s (%s) for %s' % (years[year], year, candidate_replacement_year, year.replace('begin','end'), musno)
            years[year] = candidate_replacement_year
        new_years.append(years[year])
    return new_years


with open(sys.argv[2], 'wb') as f2:
    file_with_integer_times = UnicodeWriter(f2, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
    with open(sys.argv[1], 'r') as f1:
        reader = UnicodeReader(f1, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
        try:
            for i,row in enumerate(reader):
                if i == 0:
                    date_rows, int_year_names  = get_date_rows(row)
                else:
                    row[object_materials_column] = fix_materials(row[object_materials_column])
                    row[object_name_column] = fix_name(row[object_name_column])
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
        
        
