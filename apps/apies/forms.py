import re
import time

from django import forms
import eveapi

from apps.apies.models import Api
from apps.characters.models import Character


class ApiForm(forms.Form):
    key_ID = forms.CharField(min_length=7, max_length=7, required=True)
    verification_code = forms.CharField(min_length=64, max_length=64, required=True)
    
    def clean_key_ID(self):
        data = self.cleaned_data['key_ID']
        try:
            int(data)
        except ValueError:
            raise forms.ValidationError("Should contain 7 numbers")
        return data
        
    
    def clean_verification_code(self):
        data = self.cleaned_data['verification_code']
        if not re.match("^[A-Za-z0-9]*$", data):
            raise forms.ValidationError("Should only contain 64 letters and numbers")
        return data
    
    
    def clean(self):
        key = self.cleaned_data['key_ID']
        vcode = self.cleaned_data['verification_code']
        
        if Api.objects.filter(key=key, vcode=vcode).exists():
            raise forms.ValidationError("This key has already been entered")
        
        #connect with api and validate key
        api = eveapi.EVEAPIConnection()
        auth = api.auth(keyID=key, vCode=vcode)
        try:
            keyinfo = auth.account.APIKeyInfo()
        except RuntimeError:
            raise forms.ValidationError("Invallid data, cannot connect to api")

        
    def save(self, user):
        key = self.cleaned_data['key_ID']
        vcode = self.cleaned_data['verification_code']
        
        #connect with api and validate key
        api = eveapi.EVEAPIConnection()
        auth = api.auth(keyID=key, vCode=vcode)
        keyinfo = auth.account.APIKeyInfo().key.type
        
        api = Api.objects.create(
            user = user,
            key = key,
            vcode = vcode,
            category = keyinfo,
            expires = auth.account.APIKeyInfo().key.expires,
            
        )
        
        #create related data tables
        api.create_related()
        
        #add acces run task asynchrone
        #TODO Make it asyncrone
        api.set_acces_fields()
        
    
    
    
#http://eve-prosper.blogspot.nl/2014/01/everything-you-never-wanted-to-know.html
#https://github.com/ntt/eveapi/blob/master/apitest.py
#http://wiki.eve-id.net/APIv2_Page_Index#Character
