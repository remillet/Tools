# hacks to repair data before it goes into solr

def last_name_first(name):
    if name == '': return ''
    name_parts = name.split(' ')
    return '%s, %s' % (name_parts[-1], ' '.join(name_parts[:-1]))


def rotate(l, n):
    return l[n:] + l[:n]


def fix_materials(field):
    fields = field.split('|')
    fields = [f.capitalize() for f in fields]
    field = '|'.join(fields)
    return field


def fix_name(field):
    field = field.capitalize()
    return field


def fix_proper_name(field):
    fields = field.split('|')
    fields = [last_name_first(f) for f in fields]
    field = '|'.join(fields)
    return field


def fix_culture(field):
    return field.replace('@', '').replace('Cultural and Chronological Periods|', '')
