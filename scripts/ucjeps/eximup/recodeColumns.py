import csv
import sys, os
from copy import deepcopy
from xml.sax.saxutils import escape

import time, datetime

from unicode_hack import UnicodeReader, UnicodeWriter

import re


def load_mapping_file(mapping_file):
    delim = '\t'
    cspace_mapping = {}
    with open(mapping_file, 'r') as f1:
        reader = UnicodeReader(f1, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
        for lineno, row in enumerate(reader):
            try:
                if len(row) != 9: continue
                if row[1] != '' and row[1][0] == '#': continue
                # id * FIMS field name * Cspace collectionobject tag * context tag * data type * check exists? * authority * csid
                row_id, input_field, cspace_field, context_tag, data_type, check_exists, authority, authority_csid, remarks = row
                if input_field == '':
                    continue
                #input_field = input_field.lower()
                cspace_mapping[input_field] = [cspace_field, context_tag, data_type, check_exists, int(row_id)]
            except:
                print 'Error parsing row %s in mapping file' % lineno
                print row
    return cspace_mapping



class CleanlinesFile(file):
    def next(self):
        line = super(CleanlinesFile, self).next()
        return line.replace('\r', '').replace('\n', '') + '\n'


def getRecords(rawFile):
    # csvfile = csv.reader(codecs.open(rawFile,'rb','utf-8'),delimiter="\t")
    try:
        f = CleanlinesFile(rawFile, 'rb')
        csvfile = UnicodeReader(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar=chr(255))
    except IOError:
        message = 'Expected to be able to read %s, but it was not found or unreadable' % rawFile
        return message, -1
    except:
        raise

    try:
        rows = []
        cell_values = {}
        for rowNumber, row in enumerate(csvfile):
            if rowNumber == 0:
                header = row
                continue
            rows.append(row)
            for col_number, cell in enumerate(row):
                if cell == "#": continue  # skip comments
                col_name = header[col_number]
                cell_values.setdefault(col_name, {})
                if not row[col_number] in cell_values[col_name]:
                    cell_values[col_name][row[col_number]] = 0
                    #cell_values[col_name]['bcid'] = row[0]
                cell_values[col_name][row[col_number]] += 1
        return header, rows, cell_values, len(rows)
    except IOError:
        raise
        message = 'could not read (or maybe parse) rows from %s' % rawFile
        return message, -1
    except:
        raise

if __name__ == "__main__":

    header = "*" * 80

    if len(sys.argv) < 6:
        print('%s <DWC input file> <mapping file> <template> <output file>') % sys.argv[0]
        sys.exit()

    print header
    print "RECODECOLUMNS: input  file:    %s" % sys.argv[1]
    print "RECODECOLUMNS: values file:    %s" % sys.argv[2]
    print "RECODECOLUMNS: output file:    %s" % sys.argv[3]
    print header

    try:
        column_header, rows, fimsRecords, lines = getRecords(sys.argv[1])
        print 'RECODECOLUMNS: %s lines and %s records found in file %s' % (lines, len(fimsRecords), sys.argv[1])
        print header
        if lines == -1:
            print 'RECODECOLUMNS: Error! %s' % fimsRecords
            sys.exit()
    except:
        print "RECODECOLUMNS: could not get Darwin Core ('DWC') records to load"
        sys.exit()


    try:
        #h, r, mapping, numitems = getRecords(sys.argv[3])
        mapping = load_mapping_file(sys.argv[3])
        print 'RECODECOLUMNS: %s lines and %s records found in mapping file %s' % (len(mapping), len(mapping), sys.argv[3])
        # print mapping
        print header
    except:
        print "RECODECOLUMNS: could not get mapping configuration"
        sys.exit()

    try:
        outputfh = csv.writer(open(sys.argv[5], 'wb'), delimiter="\t")
    except:
        print "RECODECOLUMNS: could not open output file for write %s" % sys.argv[5]
        sys.exit()

    successes = 0
    recordsprocessed = 0
    elapsedtimetotal = time.time()
    for row in rows.items():


        outputfh.writerow(row)
        recordsprocessed += 1

    print header
    print "RECODECOLUMNS: %s records processed" % recordsprocessed
    print header