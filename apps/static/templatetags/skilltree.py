from django import template
register = template.Library()


@register.filter
def check_group(skill, path):
    return skill.skilltree(path)
