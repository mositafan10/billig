from django.core.cache import cache
from kavenegar import *
import random

def generate_otp():
    return ''.join(str(random.randint(0,9)) for _ in range(5))

def set_otp(phone_number, otp):
    key = '%s' % (phone_number)
    cache.set(key, otp, 3000)

def verify_otp(phone_number, otp):
    key = '%s' % (phone_number)
    if cache.get(key) == otp:
        return True
    else:        
        return False

# find attacker 
# what happened when same time request is received ?
def send_sms(phone_number, otp):
    text = "کد تایید بیلیگ: {}".format(otp)
    try:
        api = KavenegarAPI("77465546766556367A4E724C6575763535386B5971764D473430415857347A33727A396F506130443366493D")
        params = {
            'receptor': phone_number,
            'message' : text,
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)
    
def validate_picture(fieldfile_obj):
        filesize = fieldfile_obj.size
        KB_limit = 1000
        if KB_limit < filesize:
            raise ValidationError("Max File Size is 500kb")
            # should be translated TODO