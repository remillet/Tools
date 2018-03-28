def fix_materials(field):
    fields = field.split('|')
    fields = [ f.capitalize() for f in fields ]
    field = '|'.join(fields)
    return field

def fix_name(field):
    field = field.capitalize()
    return field

