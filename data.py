from django.contrib.auth.models import User, Group


#add user
user = User.objects.create_user("sult", "123@234.com", "1234")
user.is_superuser = True
user.save()




#/char/SkillInTraining.xml.aspx

print "Add static skills"
execfile("populate/skills.py")
execfile("populate/wallet.py")
execfile("populate/space.py")



#setup usergroups
#DRYA moderators
moderator = Group(name="moderator")
moderator.save()

#deno's Blog
deno = Group(name="deno")
deno.save()


