from datetime import datetime, timedelta

from django import template

from apps.characters.models import Character
from apps.static.models import Skill


register = template.Library()

@register.filter
def convert_date(timestamp):
    try:
        temp = datetime.fromtimestamp(timestamp)
        return temp
    except TypeError:
        return "Not in training"



@register.filter
def station_name(stationID):
    try:    
        station = Character.find_station(stationID)
        name = station.stationName
        return name
    except AttributeError:
        return "Unknown"

@register.filter
def remap_available(timestamp):
    last = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    remap = last + timedelta(days=365)
    
    if remap > now:
        return "Now available!"
    else:
        return remap


@register.filter
def skill_name(typeID):
    skill = Skill.objects.get(typeID=typeID)
    return skill.typeName


@register.filter
def jump_fatigue(seconds):
    return datetime.now() + timedelta(seconds=seconds)
    
    
