from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, ListAttribute, UnicodeSetAttribute


class UserModel(Model):

    class Meta:
        table_name = "GolfGeorgiaPhones"

    userid = UnicodeAttribute(hash_key=True)
    phoneNumber = UnicodeAttribute()
    #Status = UnicodeAttribute()

def write_user(deviceId,phone):
    """
    returns ok
    """

    post_user = UserModel(deviceId,phoneNumber=phone)
    post_user.save()
    return 'ok'


def check_phone(deviceId):
    """
    returns True if phone in DB , False if not
    """
    try:
        check_deviceid = UserModel.get(deviceId)
        return True
    except UserModel.DoesNotExist:
        return False
