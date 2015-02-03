from collections import namedtuple, OrderedDict
from datetime import datetime
from operator import attrgetter


from django.db import models
from django.contrib.auth.models import User
import eveapi

from apps.apies.models import Api
from apps.static.models import WalletRefTypes, ConquerableStation, Skill, SkillGroup
from utils.sqlite import get_single_row


class Character(models.Model):
    """ charactertype apis """
    
    user = models.ForeignKey(User)
    api = models.ForeignKey(Api)
    
    characterID = models.IntegerField()
    name = models.CharField(max_length=254)
    corporationID = models.IntegerField()
    corporationName = models.CharField(max_length=254)
    
    
    def __unicode__(self):
        return self.name
    
    
    #get character portrait adress (128x128px)
    def portrait(self):
        return "http://image.eveonline.com/Character/%d_128.jpg" % self.characterID
    
    #get character portrait adress (128x128px)
    def portrait_big(self):
        return "http://image.eveonline.com/Character/%d_200.jpg" % self.characterID
    
    #connect to eveapi
    def auth(self):
        api = eveapi.EVEAPIConnection()
        a = api.auth(keyID=self.api.key, vCode=self.api.vcode)
        return a
        
    
    #get account balance
    def account_balance(self):
        try:
            for temp in self.auth().char.AccountBalance(characterID=self.characterID).accounts:
                balance = temp.balance
            return balance
        except eveapi.Error, e:
            print "eveapi vomit: %s\t%s" % (e.code, e.message)
        except Exception, e:
            print "critical failure: %s" % e
    
    
    #get characterinformation
    def characterSheet(self):
        auth = self.auth()
        CharacterSheet = namedtuple("CharacterSheet", "info sheet account portrait")
        char = CharacterSheet(
            portrait = self.portrait_big(),
            account = auth.account.AccountStatus(),
            info = auth.eve.CharacterInfo(characterID=self.characterID),
            sheet = auth.char.CharacterSheet(characterID=self.characterID),
        )
        
        return char

    
    #def character skills
    def characterSkills(self):
        auth = self.auth()
        sheet = auth.char.CharacterSheet(characterID=self.characterID)
        groups = SkillGroup.objects.exclude(groupName="Fake Skills").order_by("groupName")
        skills = Skill.objects.order_by("typeName")
        group_dict = OrderedDict()
        
        for group in groups:
            group_dict[group.groupName] = list()
        
        
        for skill in skills:
            trained = sheet.skills.Get(skill.typeID, False)
            if trained:
                #TODO: Add % trained to next level
                group_dict[skill.skillGroup.groupName].append({"name": skill.typeName, "level": trained.level})
                # = group_dict[skill.skillGroup.groupName].append(
        
        return group_dict
            
        
            
    #get skillqueue
    def skillQueue(self):
        auth = self.auth()
        queue = auth.char.SkillQueue(characterID=self.characterID).skillqueue
        return queue
    
    
    #get transaction row amount
    @staticmethod
    def transaction_rows(**kwargs):
        if "rows" in kwargs:
            return kwargs["rows"]
        else:
            return 50
    
    
    #convert date seconds to datetime
    @staticmethod
    def convert_date(seconds):
        return datetime.fromtimestamp(seconds)
    
    
    #get charactername from id
    @staticmethod
    def name_from_id(characterID, auth):
        return auth.eve.CharacterInfo(characterID=characterID).characterName
    
    
    # get wallet journal
    def journal_transactions(self, **kwargs):
        rowCount = self.transaction_rows(kwargs=kwargs)
        auth = self.auth()
        Transaction = namedtuple("Transaction", "date from_owner to_owner argname amount balance")
        transactions = auth.char.WalletJournal(characterID=self.characterID, rowCount=50).transactions
        transaction_list = []
        for t in transactions:
            transaction_list.append(Transaction(
                date = self.convert_date(t.date),
                from_owner = t.ownerName1,
                to_owner = t.ownerName2,
                argname = WalletRefTypes.objects.get(refTypeID=t.refTypeID).refTypeName,
                amount = t.amount,
                balance = t.balance,
            ))
        
        sorted_list = sorted(transaction_list, key=attrgetter("date"), reverse=True)
        return sorted_list
    
    
    
    # get wallet market transactions
    def market_transactions(self, **kwargs):
        rowCount = self.transaction_rows(kwargs=kwargs)
        auth = self.auth()
        Transaction = namedtuple("Transaction", "date transaction total")
        transactions = auth.char.WalletTransactions(characterID=self.characterID, rowCount=500).transactions
        transaction_list = []
        for t in transactions:
            transaction_list.append(Transaction(
                date = self.convert_date(t.transactionDateTime),
                transaction = t,
                total = t.price * t.quantity,
            ))
        
        sorted_list = sorted(transaction_list, key=attrgetter("date"), reverse=True)
        return sorted_list
    
    
    #find station by ID
    @staticmethod
    def find_station(stationID):
        station = get_single_row(kwargs={"table": "staStations", "field": "stationID", "pk": stationID})
        if station == None:
            try:
                station = ConquerableStation.objects.get(stationID=stationID)
                return station
            except ConquerableStation.DoesNotExist:
                print "fuck geen station?"
                return None
        else:
            return station
        
    
    # get wallet market transactions
    def market_orders(self):
        auth = self.auth()
        Transaction = namedtuple("Transaction", "date tipe order each issued station")
        orders = auth.char.MarketOrders(characterID=self.characterID).orders
        order_list = []
        for o in orders:
            station = self.find_station(o.stationID)
            
            order_list.append(Transaction(
                date = self.convert_date(o.issued),
                each = int(o.price / o.volEntered),
                tipe = get_single_row(kwargs={"table": "invTypes", "field": "typeID", "pk": o.typeID}),
                issued = self.convert_date(o.issued),
                order = o,
                station = station,
                
            ))
        
        sorted_list = sorted(order_list, key=attrgetter("issued"), reverse=True)
        return sorted_list
        
    
    
    def kill_log(self):
        auth = self.auth()
        return auth.char.KillLog(characterID=self.characterID).kills
        
        
    
