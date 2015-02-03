from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages

from apps.users.forms import LoginForm, RegistrationForm, ContactMailForm


def index(request):
    login_form = LoginForm(request.POST or None)
    
    if request.POST and login_form.is_valid():
        user = login_form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next') or reverse('index'))      

    return render(request, "users/index.html", {"login_form": login_form, 'next': request.GET.get('next', '')})



# Register new user
def register_user(request):
    #make sure user is not already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("index"))
    
    form = RegistrationForm(request.POST or None)
    login_form = LoginForm()
    # False till someone fills in and sends
    if request.POST and form.is_valid():
        new_user = form.save()
        #send confiermationmail blabla
        
        return HttpResponseRedirect(reverse('register succes'))
    
    return render(request, 'users/register.html', {'form': form, "login_form": login_form})
    


def register_succes(request):
    login_form = LoginForm(request.POST or None)
    return render(request, "users/register_succes.html", {"login_form": login_form})



@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))



########### Information pages

def contact(request):
    login_form = LoginForm()
    contact_form = ContactMailForm(request.POST or None)
    if request.POST and contact_form.is_valid():
        contact_form.save()
        messages.add_message(request, messages.SUCCESS, 'You will receive a reply shortly.')
        
    
    return render(request, "users/contact.html", {"login_form": login_form, "contact_form": contact_form})
