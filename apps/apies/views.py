from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
#from django.contrib import messages

from apps.apies.models import Api
from apps.apies.forms import ApiForm


@login_required
def apies(request):
    api_form = ApiForm(request.POST or None)
    
    if request.POST and api_form.is_valid():
        api_form.save(request.user)
        api_form = ApiForm()
    
    apies = Api.objects.filter(user=request.user)
    return render(request, "apies/apies.html", {"api_form": api_form, "apies": apies})
    
 
    
@login_required
def delete_api(request, pk):
    api = get_object_or_404(Api, pk=pk, user=request.user)
    api.delete_related()
    api.delete()
    
    if "charpk" in request.session:
        del request.session['charpk']
        del request.session['acces']
    
    return HttpResponseRedirect(reverse("apies"))


@login_required
def update_api(request, pk):
    api = get_object_or_404(Api, pk=pk, user=request.user)
    api.update()
    
    if "charpk" in request.session:
        del request.session['charpk']
        del request.session['acces']
        
    return HttpResponseRedirect(reverse("apies"))
