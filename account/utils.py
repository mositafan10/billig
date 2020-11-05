from django.core.cache import cache
from rest_framework.exceptions import APIException
from Basteh.settings import kavenegar_api
import random, requests

class OTP(object):
    def generate_otp():
        return (str(random.randint(1,9)) + ''.join(str(random.randint(1,9))).join(str(random.randint(0,9)) for _ in range(3)))

    def set_otp(phone_number, otp):
        key = '%s' % (phone_number)
        cache.set(key, otp, 3000)

    def verify_otp(phone_number, otp):
        key = '%s' % (phone_number)
        return cache.get(key) == otp


# find attacker 
# what happened when same time request is received ?
def send_sms(phone_number, otp):
    text = "کد تایید بیلیگ: {}".format(otp)
    try:
        data = {
            'receptor': phone_number,
            'token' : otp,
            'template' : "verify"
        }
        r = requests.post('https://api.kavenegar.com/v1/{}/verify/lookup.json'.format(kavenegar_api), data=data).json()
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

def validate_phonenumber(phone_number):
    new_phone_number = str(phone_number)
    if phone_number[0] == '9' and phone_number[1] == '8':
        if phone_number[2] == '0' :
            new_phone_number = phone_number.replace('0','',1)
    else:
        new_phone_number = '0' + '0' + phone_number
    return new_phone_number


##incompleted
def countrycode(phone_number):
    r = requests.get('https://restcountries.eu/rest/v2/callingcode/{}'.format(code))
    print(r)