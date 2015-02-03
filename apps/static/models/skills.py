from collections import OrderedDict

from django.db import models

from apps.static.models.characters import Attribute


class SkillGroup(models.Model):
    """ All skill groups """
    
    #skillGroups
    groupID = models.IntegerField()
    groupName = models.CharField(max_length=254, unique=True)
    
    def __unicode__(self):
        return self.groupName
    
    #create skilltree dictionary for template
    @staticmethod
    def skilltree_dict():
        temp = OrderedDict()
        
        for g in SkillGroup.objects.exclude(groupName="Fake Skills").order_by("groupName"):
            temp[g.groupName] = Skill.objects.filter(skillGroup=g, published=1).order_by("typeName")
        
        return temp
    


class Skill(models.Model):
    """ An eve online skill """
    
    #skills
    typeID = models.IntegerField(unique=True)
    typeName = models.CharField(max_length=254)
    published = models.IntegerField()
    skillGroup = models.ForeignKey(SkillGroup)
    description = models.TextField()
    rank = models.IntegerField()
    primaryAttribute = models.ForeignKey(Attribute, related_name="+")
    secondaryAttribute = models.ForeignKey(Attribute, related_name="+")
    
    def __unicode__(self):
        return self.typeName
    
    #get skilltree path of skill (needed for template)
    def skilltree(self, path):
        pk = int(path.split("/")[3])
        skill = Skill.objects.get(pk=pk)
        return skill.skillGroup.groupName
    
    
    
class RequiredSkill(models.Model):
    """ skill requirements """
    
    skill = models.ForeignKey(Skill, related_name="required_skills")
    required = models.ForeignKey(Skill, related_name="required")
    skillLevel = models.IntegerField()

    def __unicode__(self):
        return "requirement for %s" % self.skill.typeName
        
        
    #show level in roman
    def show_level(self):
        if self.skillLevel == 1:
            return "I"
        elif self.skillLevel == 2:
            return "II"
        elif self.skillLevel == 3:
            return "III"
        elif self.skillLevel == 4:
            return "IV"
        elif self.skillLevel == 5:
            return "V"
    
    

class SkillBonus(models.Model):
    """ bonus values of skills (per skilllevel) """
    
    skill = models.ForeignKey(Skill)
    bonusType = models.CharField(max_length=254)
    bonusValue = models.FloatField()
    
    
        
        
        
        
        
        
        
        
    
    
