from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password
from fcm_django.models import FCMDevice

from rest_framework.exceptions import APIException, NotFound

from Basteh.settings import kavenegar_api
import random, requests, string, json

def generate_otp():
    return (str(random.randint(1,9)) + ''.join(str(random.randint(1,9))).join(str(random.randint(0,9)) for _ in range(2)))

def set_otp(phone_number, otp):
    key = '%s' % (phone_number)
    cache.set(key, otp, 3000)

def verify_otp(phone_number, otp):
    key = '%s' % (phone_number)
    return cache.get(key) == otp

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
    
def validate_picture(fieldfile_obj):
        filesize = fieldfile_obj.size
        KB_limit = 1000
        if KB_limit < filesize:
            raise ValidationError("Max File Size is 500kb")


def validate_phonenumber(phone_number):
    new_phone_number = str(phone_number)
    if phone_number[0] == '9' and phone_number[1] == '8':
        if phone_number[2] == '0' :
            new_phone_number = phone_number.replace('0','',1)
    else:
        new_phone_number = '0' + '0' + phone_number
    return new_phone_number


def locate_ip(ip):
    r = requests.get('http://ip-api.com/json/{}'.format(ip)).json()
    country = None
    if r['status'] == "success":
        country = r["country"]
    return country
    
def generate_slug():
    return ''.join(str(random.choice(string.ascii_uppercase + string.ascii_lowercase)) for _ in range(8))

def send_chat_notification(user):
    try:
        fcm = FCMDevice.objects.filter(user=user)
        for i in fcm:
            header = {
                'Content-Type'  : 'application/json',
                'Authorization' : 'key=AAAA6996axw:APA91bFlpMzzDLWtxzPGyo7LAL8JVxSQ8MDt8J1cZP5FQixZ3RME_58tb1eQloxcxeFclClmvS8Y2SkOr5IAmUhzXl33joz9-hvfPzsSm_CqveSKcoDgfvyAomYRcaIjCfkgdcmOcfQ8'}
            data = {
                "notification": {
                    "title": "بیلیگ",
                    "body": "شما پیام جدید دارید",
                    "click_action": "https://billlig.com/profile/inbox",
                    "icon": "http://url-to-an-icon/icon.png"
                    },
                "to": i.registration_id
                }
            r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=header)
    except FCMDevice.DoesNotExist:
        raise NotFound(detail="پیدا نشد")


def send_offer_notification(user):
    try:
        fcm = FCMDevice.objects.filter(user=user)
        for i in fcm:
            header = {
                'Content-Type'  : 'application/json',
                'Authorization' : 'key=AAAA6996axw:APA91bFlpMzzDLWtxzPGyo7LAL8JVxSQ8MDt8J1cZP5FQixZ3RME_58tb1eQloxcxeFclClmvS8Y2SkOr5IAmUhzXl33joz9-hvfPzsSm_CqveSKcoDgfvyAomYRcaIjCfkgdcmOcfQ8'}
            data = {
                "notification": {
                    "title": "بیلیگ",
                    "body": "شما پیام جدید دارید",
                    "click_action": "https://billlig.com/profile/inbox",
                    "icon": "http://url-to-an-icon/icon.png"
                    },
                "to": i.registration_id
                }
            r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=header)
    except FCMDevice.DoesNotExist:
        raise NotFound(detail="پیدا نشد")