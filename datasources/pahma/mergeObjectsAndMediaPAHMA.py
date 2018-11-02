
import sys, csv
from collections import defaultdict
from unicode_hack import UnicodeReader, UnicodeWriter

count = defaultdict(int)
delim = '\t'

# MEDIA = open(sys.argv[1],'r')
# die "couldn't open media file sys.arg[0]"
blobs = defaultdict()
seen = defaultdict()
# this needs to be a list
restricted = ['59a733dd-d641-4e1a-8552']

mimetypes = {'application/pdf': 'pdf',
             'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'msword',
             'audio/mpeg': 'audio',
             'audio/x-wav': 'audio',
             'image/jpeg': 'image',
             'image/photoshop': 'other',
             'image/png': 'image',
             'image/tiff': 'image',
             'image/x-adobe-dng': 'other',
             'image/x-nikon-nef': 'other',
             'video/mp4': 'video'}

runtype = sys.argv[3]  # generate media for public or internal

fcpcol = 39
contextofusecol = 13
objectnamecol = 8


def check(string_to_check, pattern):
    if unicode(pattern) in unicode(string_to_check):
        return True
    else:
        return False

writer = UnicodeWriter(open(sys.argv[4], "wb"), delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))

with open(sys.argv[1], 'r') as MEDIA:
    reader = UnicodeReader(MEDIA, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
    for row in reader:

        count['media'] += 1
        if len(row) != 17:
            print row
            continue
        (objectcsid, objectnumber, mediacsid, description, name, creatorrefname, creator, blobcsid, copyrightstatement,
         identificationnumber, rightsholderrefname, rightsholder, contributor, approvedforweb, pahmatmslegacydepartment,
         objectstatus, primarydisplay) = row
        # , mimetype
        mimetype = 'image/jpeg'
        # print "blobcsid objectcsid\n"
        imagetype = 'images'
        # mark catalog card images as such
        if check(description, '(catalog card|HSR Datasheet)'): imagetype = 'cards'
        if check(description, '^Index'): imagetype = 'cards'
        ispublic = 'public'
        # we don't need to match a pattern here, it's a vocabulary. But just in case...
        if check(pahmatmslegacydepartment, 'Human Remains'): ispublic = 'notpublic'
        if check(pahmatmslegacydepartment, 'NAGPRA-associated Funerary Objects'): ispublic = 'notpublic'
        if check(objectstatus, 'culturally'): ispublic = 'notpublic'
        # NB: the test 'burial' in context of use occurs below -- we only mask if the FCP is in North America
        if not (approvedforweb == 't'): ispublic = 'notpublic'
        # ispublic = 'notapprovedforweb' unless (approvedforweb == 't')
        if (imagetype == 'cards'): ispublic = 'public'
        # warn ispublic + imagetype
        count[imagetype] += 1
        count[ispublic] += 1
        # start by assuming no images for this object
        # blobs[objectcsid]['hasimages'] = 'no'
        blobs[objectcsid] = defaultdict(int)
        blobs[objectcsid]['cards'] = []
        blobs[objectcsid]['images'] = []
        blobs[objectcsid]['type'] = []
        blobs[objectcsid]['restrictions'] = []
        if (imagetype == 'cards'):
            blobs[objectcsid]['cards'].append(blobcsid)
        else:
            blobs[objectcsid]['hasimages'] = 'yes'
            # if this run is to generate the public datastore, use the restricted image if this blob is restricted.
            if (runtype == 'public'):
                if (ispublic != 'public'): blobcsid = restricted

            if (primarydisplay == 't'):
                blobs[objectcsid]['primary'] = blobcsid

                # add this blob to the list of blobs, unless we somehow already have it (no dups allowed!)
                if not check(blobs[objectcsid]['images'], 'blobcsid'):
                    # put primary images first
                    if (primarydisplay == 't'):
                        blobs[objectcsid]['images'].insert(0, blobcsid)

                    else:
                        blobs[objectcsid]['images'].append(blobcsid)
        if not check(blobs[objectcsid]['type'], 'imagetype'): blobs[objectcsid]['type'].append(imagetype)
        if not check(blobs[objectcsid]['restrictions'], 'ispublic'): blobs[objectcsid]['restrictions'].append(ispublic)

# die "couldn't open metadata file sys.arg[1]"

with open(sys.argv[2], 'r') as METADATA:
    reader = UnicodeReader(METADATA, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
    for line in reader:
        id = line[0]
        objectcsid = line[1]
        rest = line[2:]
        if (objectcsid == ''):
            print "objectcsid is blank: "
            continue
        # handle header line
        if (id == 'id'):
            header = line + u'blob_ss,card_ss,primaryimage_s,imagetype_ss,restrictions_ss,hasimages_s'.split(',')
            writer.writerow(header)
            continue
        count['metadata'] += 1
        mediablobs = line
        if (objectcsid in blobs):
            if (runtype == 'public'):
                # if context of use field contains the word burial
                if check(rest[contextofusecol], 'burial') and check(rest[fcpcol], 'United States') and \
                        blobs[objectcsid]['images'] != []: blobs[objectcsid]['images'] = restricted
                # if object name contains something like "charm stone"
                if check(rest[objectnamecol], 'charm.*stone') and check(rest[fcpcol], 'United States') and \
                        blobs[objectcsid]['images'] != []: blobs[objectcsid]['images'] = restricted
                # belt-and-suspenders: restrict if charm stone or NAGPRA appear anywhere in USA records...
                if check(line, '(charm.*stone|NAGPRA-associated Funerary Objects)') and check(rest[fcpcol],'United States') and \
                        blobs[objectcsid]['images'] != []: blobs[objectcsid]['images'] = restricted

            # insert list of blobs, etc. as final columns
            # blobs[objectcsid]['restrictions']
            # blobs[objectcsid]['type']
            blobs[objectcsid]['type'] = blobs[objectcsid]['type'].split(',').join(',')
            if not blobs[objectcsid]['hasimages'] == 'yes': blobs[objectcsid]['hasimages'] = 'no'
            count['hasimages: ' + blobs[objectcsid]['hasimages']] += 1
            for column in 'images cards primary type restrictions hasimages'.split(' '):
                mediablobs.append(blobs[objectcsid][column])

            count['object type: ' + blobs[objectcsid]['type']] += 1
            count['object restrictions: ' + blobs[objectcsid]['restrictions']] += 1
            count['matched: yes'] += 1
        else:
            count['matched: no'] += 1
            count['hasimages: no'] += 1
            mediablobs += [''] * 6
            mediablobs += 'no'

        writer.writerow(mediablobs)

for s in count.keys():
    print "%s: %s" % (s, count[s])
