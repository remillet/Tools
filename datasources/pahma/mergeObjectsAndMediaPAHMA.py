
import sys, csv
from collections import defaultdict
from unicode_hack import UnicodeReader, UnicodeWriter

count = defaultdict(int)
delim = '\t'

blobs = defaultdict()
seen = defaultdict()
restricted = '59a733dd-d641-4e1a-8552'

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
    if unicode(pattern).lower() in unicode(string_to_check).lower():
        return True
    else:
        return False

writer = UnicodeWriter(open(sys.argv[4], "wb"), delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))

with open(sys.argv[1], 'r') as MEDIA:
    reader = UnicodeReader(MEDIA, delimiter=delim, quoting=csv.QUOTE_NONE, quotechar=chr(255))
    for row in reader:

        count['media'] += 1

        # skip header row
        if count['media'] == 1:
            continue

        if len(row) != 18:
            print row
            count['skipped media (invalid row)'] += 1
            continue
        (objectcsid, objectnumber, mediacsid, description, name, creatorrefname, creator, blobcsid, copyrightstatement,
         identificationnumber, rightsholderrefname, rightsholder, contributor, approvedforweb, pahmatmslegacydepartment,
         objectstatus, primarydisplay, mimetype) = row
        count['primary display %s' % primarydisplay] += 1
        count['mimetype %s' % mimetype] += 1
        if mimetype in mimetypes:
            available_media = mimetypes[mimetype]
        else:
            available_media = 'unrecognized'
        count['media available %s' % available_media] += 1
        # print "blobcsid objectcsid\n"
        media_type = 'images'
        # mark catalog card images as such
        if check(description, 'catalog card') or check(description, 'HSR Datasheet'): media_type = 'legacy documentation'
        if check(description, 'Index'): media_type = 'legacy documentation'
        ispublic = 'public'
        # we don't need to match a pattern here, it's a vocabulary. But just in case...
        if check(pahmatmslegacydepartment, 'Human Remains'): ispublic = 'notpublic'
        if check(pahmatmslegacydepartment, 'NAGPRA-associated Funerary Objects'): ispublic = 'notpublic'
        if check(objectstatus, 'culturally'): ispublic = 'notpublic'
        # NB: the test 'burial' in context of use occurs below -- we only mask if the FCP is in North America
        if not (approvedforweb == 't'): ispublic = 'notpublic'
        # ispublic = 'notapprovedforweb' unless (approvedforweb == 't')
        if (media_type == 'legacy documentation'): ispublic = 'public'
        # warn ispublic + imagetype
        count[media_type] += 1
        count[ispublic] += 1
        # start by assuming no images for this object
        # blobs[objectcsid]['hasimages'] = 'no'
        if not objectcsid in blobs:
            blobs[objectcsid] = defaultdict(int)
            blobs[objectcsid]['legacy documentation'] = []
            blobs[objectcsid]['images'] = []
            blobs[objectcsid]['type'] = []
            blobs[objectcsid]['restrictions'] = []
            blobs[objectcsid]['video_csids'] = []
            blobs[objectcsid]['video_mimetypes'] = []
            blobs[objectcsid]['audio_csids'] = []
            blobs[objectcsid]['audio_mimetypes'] = []
            blobs[objectcsid]['d3_csids'] = []
            blobs[objectcsid]['d3_mimetypes'] = []
            blobs[objectcsid]['media_available'] = []
            blobs[objectcsid]['mimetypes'] = []
            blobs[objectcsid]['primary'] = ''

        if not check(blobs[objectcsid]['mimetypes'], mimetype):
            blobs[objectcsid]['mimetypes'].append(mimetype)
        if not check(blobs[objectcsid]['media_available'], available_media):
            blobs[objectcsid]['media_available'].append(available_media)

        if (available_media in ['audio','video','d3']):
            if ispublic == 'public':
                blobs[objectcsid]['%s_csids' % available_media].append(blobcsid)
                blobs[objectcsid]['%s_mimetypes' % available_media].append(mimetype)

        if (media_type == 'legacy documentation'):
            blobs[objectcsid]['legacy documentation'].append(blobcsid)

        else:
            blobs[objectcsid]['hasimages'] = 'yes'
            # if this run is to generate the public datastore, use the restricted image if this blob is restricted.
            if (runtype == 'public'):
                if (ispublic != 'public'): blobcsid = restricted

            # add this blob to the list of blobs, unless we somehow already have it (no dups allowed!)
            if not check(blobs[objectcsid]['images'], blobcsid):
                # put primary images first
                if (primarydisplay == 't'):
                    blobs[objectcsid]['images'].insert(0, blobcsid)
                    blobs[objectcsid]['primary'] = blobcsid

                else:
                    blobs[objectcsid]['images'].append(blobcsid)

        if not check(blobs[objectcsid]['type'], media_type): blobs[objectcsid]['type'].append(media_type)
        if not check(blobs[objectcsid]['restrictions'], ispublic): blobs[objectcsid]['restrictions'].append(ispublic)

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
            header = line + u'blob_ss,card_ss,primaryimage_s,imagetype_ss,restrictions_ss,hasimages_s,video_csid_ss,video_mimetype_ss,audio_csid_ss,audio_mimetype_ss,d3_csid_ss,d3_mimetype_ss,media_available_ss,mimetypes_ss'.split(',')
            writer.writerow(header)
            continue
        count['metadata'] += 1
        mediablobs = line
        if (objectcsid in blobs):
            if (runtype == 'public'):
                # for US sites...
                if check(rest[fcpcol], 'United States') and blobs[objectcsid]['images'] != []:
                    line_as_string = ' '.join(line)
                    # if context of use field contains the word burial
                    if check(rest[contextofusecol], 'burial'):
                        blobs[objectcsid]['images'] = restricted
                    # if object name contains something like "charm stone"
                    elif (check(rest[objectnamecol], 'charm stone') or check(rest[objectnamecol], 'charmstone')):
                        blobs[objectcsid]['images'] = restricted
                    # belt-and-suspenders: restrict if charm stone or NAGPRA appear anywhere...
                    elif (check(line_as_string, 'charm stone') or check(line_as_string, 'charmstone')):
                        blobs[objectcsid]['images'] = restricted
                    elif check(line_as_string, 'NAGPRA-associated Funerary Objects'):
                        blobs[objectcsid]['images'] = restricted

            # insert list of blobs, etc. as final columns
            if not blobs[objectcsid]['hasimages'] == 'yes': blobs[objectcsid]['hasimages'] = 'no'
            count['hasimages: %s' % blobs[objectcsid]['hasimages']] += 1
            for column in 'images,legacy documentation,primary,type,restrictions,hasimages,video_csids,video_mimetypes,audio_csids,audio_mimetypes,d3_csids,d3_mimetypes,media_available,mimetypes'.split(','):
                if type(blobs[objectcsid][column]) == type([]):
                    mediablobs.append('|'.join(sorted(blobs[objectcsid][column])))
                else:
                    mediablobs.append(blobs[objectcsid][column])

            count['object type: ' + ','.join(sorted(blobs[objectcsid]['type']))] += 1
            count['object restrictions: ' + ','.join(sorted(blobs[objectcsid]['restrictions']))] += 1
            count['matched: yes'] += 1
        else:
            count['matched: no'] += 1
            count['hasimages: no'] += 1
            mediablobs += [u''] * 4
            mediablobs += [u'public']
            mediablobs += [u'no']
            mediablobs += [u''] * 8

        for i,m in enumerate(mediablobs):
            if type(m) == type(0):
                count['repaired'] += 1
                mediablobs[i] = str(m)

        writer.writerow(mediablobs)

for s in sorted(count.keys()):
    print "%s: %s" % (s, count[s])
