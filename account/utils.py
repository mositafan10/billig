from django.core.cache import cache
from rest_framework.exceptions import APIException
from kavenegar import *
import random
from Basteh.settings.prod import kavenegar_api

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
        api = KavenegarAPI(kavenegar_api)
        params = {
            'receptor': phone_number,
            'message' : text,
        } 
        response = api.sms_send(params)
    except APIException as e: 
        pass
    except HTTPException as e: 
        pass
    
def validate_picture(fieldfile_obj):
        filesize = fieldfile_obj.size
        KB_limit = 1000
        if KB_limit < filesize:
            raise ValidationError("Max File Size is 500kb")
            # should be translated TODO