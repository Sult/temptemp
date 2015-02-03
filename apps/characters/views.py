from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


from apps.apies.models import Api
from apps.apies.forms import ApiForm
from apps.characters.models import Character


@login_required
def characters(request):
    api_form = ApiForm(request.POST or None)
    
    if request.POST and api_form.is_valid():
        api_form.save(request.user)
        api_form = ApiForm()
    
    characters = Character.objects.filter(user=request.user)
    #if request.user.groups.filter(name="moderator").exists() or request.user.is_superuser:
    #    members = Character.objects.exclude(user=request.user)
    #    return render(request, "characters/characters.html", {"api_form": api_form, "characters": characters,"members": members})
    
    return render(request, "characters/characters.html", {"api_form": api_form, "characters": characters})



@login_required
def select_character(request, pk):
    if request.user.groups.filter(name="moderator").exists() or request.user.is_superuser:
        character = get_object_or_404(Character, pk=pk)
    else:
        character = get_object_or_404(Character, pk=pk, user=request.user)    
    request.session['charpk'] = character.pk
    request.session['acces'] = character.api.acces_dict()
    return HttpResponseRedirect(reverse("character_sheet"))
        


#view basic character information
@login_required
def character_sheet(request):
    if not "charpk" in request.session:
        return HttpResponseRedirect(reverse("characters"))
    else:
        try:
            if request.user.groups.filter(name="moderator").exists() or request.user.is_superuser:
                character = Character.objects.get(pk=request.session["charpk"])
            else:
                character = Character.objects.get(pk=request.session["charpk"], user=request.user)
            auth = character.auth()
            pk = character.characterID
            if not character.api.characterInfo_acces(auth, pk) or not character.api.characterSheet_acces(auth, pk) or not character.api.accountStatus_acces(auth, pk):
                return HttpResponseRedirect(reverse("characters"))
        except Character.DoesNotExist:
            return HttpResponseRedirect(reverse("characters"))
    
    char = character.characterSheet()
    return render(request, "characters/character_sheet.html", {"char": char})
    

#view basic character information
@login_required
def character_skills(request):
    if not "charpk" in request.session:
        return HttpResponseRedirect(reverse("characters"))
    else:
        try:
            if request.user.groups.filter(name="moderator").exists() or request.user.is_superuser:
                character = Character.objects.get(pk=request.session["charpk"])
            else:
                character = Character.objects.get(pk=request.session["charpk"], user=request.user)
            if not character.api.characterInfo_acces(character.auth(), character.characterID):
                return HttpResponseRedirect(reverse("characters"))
        except Character.DoesNotExist:
            return HttpResponseRedirect(reverse("characters"))
    
    skills = character.characterSkills()
    queue = character.skillQueue()
    return render(request, "characters/character_skills.html", {"skills": skills, "queue": queue , "character": character})


#wallet journal
@login_required
def wallet_journal(request):
    if not "charpk" in request.session:
        return HttpResponseRedirect(reverse("characters"))
    else:
        try:
            if request.user.groups.filter(name="moderator").exists() or request.user.is_superuser:
                character = Character.objects.get(pk=request.session["charpk"])
            else:
                character = Character.objects.get(pk=request.session["charpk"], user=request.user)
            if not character.api.walletJournal_acces(character.auth(), character.characterID):
                return HttpResponseRedirect(reverse("characters"))
        except Character.DoesNotExist:
            return HttpResponseRedirect(reverse("characters"))
    
    if request.GET:
        #get amount of rows
        pass
    
    transactions = character.journal_transactions()
    return render(request, "characters/wallet_journal.html", {"transactions": transactions, "character": character})



#market transactions
@login_required
def market_transactions(request):
    if not "charpk" in request.session:
        return HttpResponseRedirect(reverse("characters"))
    else:
        try:
            if request.user.groups.filter(name="moderator").exists() or request.user.is_superuser:
                character = Character.objects.get(pk=request.session["charpk"])
            else:
                character = Character.objects.get(pk=request.session["charpk"], user=request.user)
            if not character.api.walletTransactions_acces(character.auth(), character.characterID):
                return HttpResponseRedirect(reverse("characters"))
        except Character.DoesNotExist:
            return HttpResponseRedirect(reverse("characters"))
    
    if request.GET:
        #get amount of rows
        pass
    
    transactions = character.market_transactions()
    return render(request, "characters/market_transactions.html", {"transactions": transactions, "character": character})



##market orders
#@login_required
#def market_orders(request):
    #if not "charpk" in request.session:
        #return HttpResponseRedirect(reverse("characters"))
    #else:
        #try:
            #character = Character.objects.get(pk=request.session["charpk"], user=request.user)
            #if not character.api.marketOrders_acces(character.auth(), character.characterID):
                #return HttpResponseRedirect(reverse("characters"))
        #except Character.DoesNotExist:
            #return HttpResponseRedirect(reverse("characters"))

    #orders = character.market_orders()
    #return render(request, "characters/market_orders.html", {"orders": orders, "character": character})




#market orders
@login_required
def character_killboard(request):
    if not "charpk" in request.session:
        return HttpResponseRedirect(reverse("characters"))
    else:
        try:
            if request.user.groups.filter(name="moderator").exists() or request.user.is_superuser:
                character = Character.objects.get(pk=request.session["charpk"])
            else:
                character = Character.objects.get(pk=request.session["charpk"], user=request.user)
            if not character.api.marketOrders_acces(character.auth(), character.characterID):
                return HttpResponseRedirect(reverse("characters"))
        except Character.DoesNotExist:
            return HttpResponseRedirect(reverse("characters"))

    kill_log = character.kill_log()
    return render(request, "characters/killboard.html", {"character": character, "kill_log": kill_log})


