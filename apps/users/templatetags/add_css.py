from django import template
register = template.Library()

@register.filter
def addcss(field, css):
    return field.as_widget(attrs={"class":css})


@register.filter
def space_to_underscore(string):
    return string.replace(" ", "_")



#loop over queryset in groups of n
def grouped(l, n):
    # Yield successive n-sized chunks from l.
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

@register.filter
def group_by(value, arg):
    return grouped(value, arg)
    
    
