import eveapi
import xml.etree.ElementTree as ET

from apps.static.models import Skill, SkillGroup, Attribute, RequiredSkill, SkillBonus



def skill_groups():
    api = eveapi.EVEAPIConnection()
    skilltree = api.eve.SkillTree()
    
    for g in skilltree.skillGroups:
        try:
            SkillGroup.objects.create(
                groupID = g.groupID,
                groupName = g.groupName,
            )
        except:
            pass



def attributes():
    api = eveapi.EVEAPIConnection()
    skilltree = api.eve.SkillTree()
    
    for g in skilltree.skillGroups:
        for skill in g.skills:
            try:
                Attribute.objects.create(
                    name=skill.requiredAttributes.secondaryAttribute,
                )
            except:
                pass


tree = ET.parse("populate/skilltree.xml")
root = tree.getroot()
#https://docs.python.org/2/library/xml.etree.elementtree.html#xpath-support
def get_description(typeID):
    for result in root.findall("result"):
        for rowset in result.findall("rowset"):
            for row in rowset.findall("row"):
                for rw in row.findall("rowset"):
                    for r in rw.findall("row"):
                        if r.get("typeID") == str(typeID):
                            return r.find("description").text




def skills():
    api = eveapi.EVEAPIConnection()
    skilltree = api.eve.SkillTree()
    
    for g in skilltree.skillGroups:
        #get skillgroup
        skillgroup = SkillGroup.objects.get(groupID=g.groupID)
        
        for skill in g.skills:
            
            try:
                
                t = type(skill.description)
                if t == unicode:
                    desc = skill.description
                else:
                    desc = get_description(skill.typeID)
                
                
                s = Skill.objects.create(
                    typeID = skill.typeID,
                    typeName = skill.typeName,
                    published=skill.published,
                    skillGroup = skillgroup,
                    description = desc,
                    rank = skill.rank,
                    primaryAttribute = Attribute.objects.get(name=skill.requiredAttributes.primaryAttribute),
                    secondaryAttribute = Attribute.objects.get(name=skill.requiredAttributes.secondaryAttribute),
                )
                
                for bonus in skill.skillBonusCollection:
                    SkillBonus.objects.create(
                        skill = s,
                        bonusType = bonus.bonusType,
                        bonusValue = bonus.bonusValue,
                    )
            except:
                print skill.typeName
            
            
            
                
def requirements():
    api = eveapi.EVEAPIConnection()
    skilltree = api.eve.SkillTree()
    
    for g in skilltree.skillGroups:
        #get skillgroup
        
        for skill in g.skills:
            try:
                s = Skill.objects.get(typeID=skill.typeID)

                for req in skill.requiredSkills:
                    RequiredSkill.objects.create(
                        skill = s,
                        required = Skill.objects.get(typeID=req.typeID),
                        skillLevel = req.skillLevel,
                    )
            except:
                print "Fake?:"
        

skill_groups()
attributes()
skills()
requirements()
