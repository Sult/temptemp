from django.db import models,IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone
import eveapi

from datetime import datetime


class Api(models.Model):
    """ charactertype apis """
    
    user = models.ForeignKey(User)
    key = models.IntegerField(verbose_name="Key ID")
    vcode = models.CharField(max_length=254, verbose_name="Verification Code")
    category = models.CharField(max_length=254)
    expires = models.CharField(max_length=254, blank=True)
    
    #account and market
    walletTransactions = models.NullBooleanField(default=None)
    walletJournal = models.NullBooleanField(default=None)
    marketOrders = models.NullBooleanField(default=None)
    accountBalance = models.NullBooleanField(default=None)
    
    #communications
    notificationTexts = models.NullBooleanField(default=None)
    notifications = models.NullBooleanField(default=None)
    mailMessages = models.NullBooleanField(default=None)
    mailingLists = models.NullBooleanField(default=None)
    mailBodies = models.NullBooleanField(default=None)
    contactNotifications = models.NullBooleanField(default=None)
    contactList = models.NullBooleanField(default=None)
    
    #private Information
    locations = models.NullBooleanField(default=None)
    contracts = models.NullBooleanField(default=None)
    accountStatus = models.NullBooleanField(default=None)
    characterInfo = models.NullBooleanField(default=None)
    upcomingCalendarEvents = models.NullBooleanField(default=None)
    skillQueue = models.NullBooleanField(default=None)
    skillInTraining = models.NullBooleanField(default=None)
    characterSheet = models.NullBooleanField(default=None)
    calendatEventAttendees = models.NullBooleanField(default=None)
    assetList = models.NullBooleanField(default=None)
    
    #public information
    standings = models.NullBooleanField(default=None)
    medals = models.NullBooleanField(default=None)
    killLog = models.NullBooleanField(default=None)
    facWarStats = models.NullBooleanField(default=None)
    
    #science and industry
    research = models.NullBooleanField(default=None)
    industryJobs = models.NullBooleanField(default=None)
    
    
    #corp acces
    corp_killLog = models.NullBooleanField(default=None)
    corp_memberTracking = models.NullBooleanField(default=None)
    
    
    
    class Meta:
        unique_together = ["key", "vcode", "user"]
    
    def __unicode__(self):
        return "Api from %s" % self.user.username
    
    #create a name for the api
    def name(self):
        if not self.category == "Corporation":
            string = self.category + " - "
            for character in self.character_set.all():
                string += character.name + ", "
            return string[:-2]
            
        else:
            
            return "Corporation: %s" % self.corporation.corporationName
    
    #string for GET use in templates
    def pk_string(self):
        return str(self.pk)
    

    #make expires a readable time in template
    def show_expires(self):
        if self.expires != "":
            temp = datetime.fromtimestamp(int(self.expires)).replace(tzinfo=timezone.utc)
            if temp > timezone.now():
                return temp
            else:
                return "Expired!"
        else:
            return "Never"


    #created related data
    def create_related(self):
        api = eveapi.EVEAPIConnection()
        auth = api.auth(keyID=self.key, vCode=self.vcode)
        keyinfo = auth.account.APIKeyInfo().key.type
        characters = auth.account.Characters().characters
        if not keyinfo == u'Corporation':
            for character in characters:
                try:
                    models.get_model("characters", "Character").objects.create(
                        user = self.user,
                        api = self,
                        characterID = character.characterID,
                        name = character.name,
                        corporationID = character.corporationID,
                        corporationName = character.corporationName,
                    )
                except IntegrityError:
                    pass
        #create corporation
        else:
            for character in characters:
                try:
                    models.get_model("corporations", "Corporation").objects.create(
                        user = self.user,
                        api = self,
                        corporationID = character.corporationID,
                        corporationName = character.corporationName,
                    )
                except IntegrityError:
                    pass
                
            
    

    #delete related api models
    def delete_related(self):
        if self.category != "Corporation":
            chars = self.character_set.all()
            chars.delete()
        else:
            #delete corporation
            pass
    
    
    #update api
    def update(self):
        self.delete_related()
        self.create_related()
        self.set_acces_fields()
    
    
    #character api connection fields
    @staticmethod
    def character_acces_fields():
        temp = ["walletTransactions", "walletJournal", "marketOrders", "accountBalance", "mailMessages", "mailingLists", "mailBodies", "accountStatus", "characterInfo", "skillQueue", "skillInTraining", "characterSheet", "assetList", "killLog"]
        return temp
    
    
    #get corp acces fields
    @staticmethod
    def corporation_acces_fields():
        temp = ["killLog", "memberTracking"]
        return temp
    
    
    #get acces dict for navbar
    def acces_dict(self):
        fields = self.character_acces_fields() #+ self.corporation_acces_fields()
        temp = {}
        for field in fields:
            temp[field] = getattr(self, field)
            
            #add collapsables
            if self.walletJournal or self.walletTransactions or self.marketOrders:
                temp["wallet"] = True
            
        return temp
            
    
    
    
    #get account type acces fields
    def set_acces_fields(self):
        api = eveapi.EVEAPIConnection()
        auth = api.auth(keyID=self.key, vCode=self.vcode)
        
        if self.category == u'Corporation':
            #Will come
            fields = Api.corporation_acces_fields()
            for field in fields:
                acces = getattr(self, "corp_" + field + "_acces")(auth, self.corporation.corporationID)
                setattr(self, field, acces)
            
        else:
            fields = Api.character_acces_fields()
            character = self.character_set.all()[0]
            for field in fields:
                acces = getattr(self, field + "_acces")(auth, character.characterID)
                setattr(self, field, acces)
        self.save()
            
            

    
    # acces functions
    def walletTransactions_acces(self, auth, characterID):
        try:
            auth.char.WalletTransactions(characterID=characterID)
            return True
        except Exception:
            return False
    def walletJournal_acces(self, auth, characterID):
        try:
            auth.char.WalletJournal(characterID=characterID)
            return True
        except Exception:
            return False
    def marketOrders_acces(self, auth, characterID):
        try:
            auth.char.MarketOrders(characterID=characterID)
            return True
        except Exception:
            return False
    def accountBalance_acces(self, auth, characterID):
        try:
            auth.char.AccountBalance(characterID=characterID)
            return True
        except Exception:
            return False
    #def notificationTexts_acces(self, auth, characterID):
        #try:
            #auth.char.NotificationTexts(characterID=characterID)
            #return True
        #except Exception:
            #return False
    #def notifications_acces(self, auth, characterID):
        #try:
            #auth.char.Notifications(characterID=characterID)
            #return True
        #except Exception:
            #return False
    def mailMessages_acces(self, auth, characterID):
        try:
            auth.char.MailMessages(characterID=characterID)
            return True
        except Exception:
            return False
    def mailingLists_acces(self, auth, characterID):
        try:
            auth.char.MailingLists(characterID=characterID)
            return True
        except Exception:
            return False
    def mailBodies_acces(self, auth, characterID):
        if self.mailMessages_acces(auth, characterID):
            try:
                ids = auth.char.MailMessages(characterID=characterID).messages
                auth.char.MailBodies(characterID=characterID, ids=ids[0].messageID).messages
                return True
            except Exception:
                return False
    #def contactNotifications_acces(self, auth, characterID):
        #try:
            #auth.char.ContactNotifications(characterID=characterID)
            #return True
        #except Exception:
            #return False
    #def contactList_acces(self, auth, characterID):
        #try:
            #auth.char.ContactList(characterID=characterID)
            #return True
        #except Exception:
            #return False
    #def contracts_acces(self, auth, characterID):
        #try:
            #auth.char.Contracts(characterID=characterID)
            #return True
        #except Exception:
            #return False
    def accountStatus_acces(self, auth, characterID):
        try:
            auth.account.AccountStatus()
            return True
        except Exception:
            return False
    def characterInfo_acces(self, auth, characterID):
        try:
            auth.eve.CharacterInfo(characterID=characterID)
            return True
        except Exception:
            return False
    #def upcomingCalendarEvents_acces(self, auth, characterID):
        #try:
            #auth.char.UpcommingCalendarEvents(characterID=characterID)
            #return True
        #except Exception:
            #return False
    def skillQueue_acces(self, auth, characterID):
        try:
            auth.char.SkillQueue(characterID=characterID)
            return True
        except Exception:
            return False
    def skillInTraining_acces(self, auth, characterID):
        try:
            auth.char.SkillInTraining(characterID=characterID)
            return True
        except Exception:
            return False
    def characterSheet_acces(self, auth, characterID):
        try:
            auth.char.CharacterSheet(characterID=characterID)
            return True
        except Exception:
            return False
    #def calendatEventAttendees_acces(self, auth, characterID):
        #try:
            #auth.char.CalendarEventAttendees(characterID=characterID)
            #return True
        #except Exception:
            #return False
    def assetList_acces(self, auth, characterID):
        try:
            auth.char.AssetList(characterID=characterID)
            return True
        except Exception:
            return False
    #def standings_acces(self, auth, characterID):
        #try:
            #auth.char.Standings(characterID=characterID)
            #return True
        #except Exception:
            #return False
    #def medals_acces(self, auth, characterID):
        #try:
            #auth.char.Medals(characterID=characterID)
            #return True
        #except Exception:
            #return False
    def killLog_acces(self, auth, characterID):
        try:
            auth.char.Killlog(characterID=characterID)
            return True
        except Exception:
            return False
    #def facWarStats_acces(self, auth, characterID):
        #try:
            #auth.char.FacWarStats(characterID=characterID)
            #return True
        #except Exception:
            #return False
    #def research_acces(self, auth, characterID):
        #try:
            #auth.char.Research(characterID=characterID)
            #return True
        #except Exception:
            #return False
    #def industryJobs_acces(self, auth, characterID):
        #try:
            #auth.char.IndustryJobs(characterID=characterID)
            #return True
        #except Exception:
            #return False



    #corporation acces
    #killboars
    def corp_killLog_acces(self, auth, corporationID):
        try:
            auth.corp.Killlog()
            return True
        except Exception:
            return False
            
    #member list
    def corp_memberTracking_acces(self, auth, corporationID):
        try:
            auth.corp.MemberTracking()
            return True
        except Exception:
            return False
