from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from apps.static.models import SkillGroup, Skill


@login_required
def tree(request):
    pk = Skill.objects.filter(published=1).order_by("?")[0]
    return HttpResponseRedirect(reverse("skilltree", kwargs={"pk": pk.pk}))



@login_required
def skilltree(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    skilltree = SkillGroup.skilltree_dict()
    return render(request, "static/skilltree.html", {"skilltree": skilltree, "skill": skill})
