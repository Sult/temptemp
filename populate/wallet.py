import eveapi
from apps.static.models import WalletRefTypes



def add_ref_types():
    api = eveapi.EVEAPIConnection()
    
    reftypes = api.eve.RefTypes().refTypes
    for ref in reftypes:
        try:
            WalletRefTypes.objects.create(
                refTypeID = ref.refTypeID,
                refTypeName = ref.refTypeName,
            )
        except:
            print "ooeps"


add_ref_types()
