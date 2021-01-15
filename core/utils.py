from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password

from fcm_django.models import FCMDevice

from rest_framework.exceptions import APIException, NotFound

from Basteh.settings import kavenegar_api
import random, requests, string, json
from .constant import Prohibited_name


def generate_otp():
    return (str(random.randint(1,9)) + ''.join(str(random.randint(1,9))).join(str(random.randint(0,9)) for _ in range(2)))


def setPhoneCache(phone_number):
    key = '%s' % (phone_number)
    if cache.get(key) is not None:
        if cache.get(key) == 1:
            cache.set(key, 2, 120)
            return True
        elif cache.get(key) == 2:
            cache.set(key, 3, 120)
            return True
        elif cache.get(key) == 3:
            return False
    else:
        cache.set(key, 1, 120)
        return True


def set_otp(phone_number, otp):
    key = '%s-%s' % (phone_number,otp)
    cache.set(key, otp, 300)


def verify_otp(phone_number, otp):
    key = '%s-%s' % (phone_number,otp)
    return cache.get(key) == otp


def send_sms(phone_number, otp):
    try:
        data = {
            'receptor': phone_number,
            'token' : otp,
            'template' : "verify"
        }
        r = requests.post('https://api.kavenegar.com/v1/{}/verify/lookup.json'.format(kavenegar_api), data=data).json()
    except: 
        pass


def send_sms_publish(phone_number, packet):
    try:
        data = {
            'receptor': phone_number,
            'token20' : packet,
            'token': "عنوان",
            'template' : "publish"
        }
        r = requests.post('https://api.kavenegar.com/v1/{}/verify/lookup.json'.format(kavenegar_api), data=data).json()
    except: 
        pass
    

def send_sms_notpublish(phone_number, packet):
    try:
        data = {
            'receptor': phone_number,
            'token20' : packet,
            'token': "عنوان",
            'template' : "Notpublish"
        }
        r = requests.post('https://api.kavenegar.com/v1/{}/verify/lookup.json'.format(kavenegar_api), data=data).json()
    except: 
        pass


def validate_picture(fieldfile_obj):
        filesize = fieldfile_obj.size
        KB_limit = 1000
        if KB_limit < filesize:
            raise ValidationError("Max File Size is 500kb")


# Should be test TODO
def validate_phonenumber(phone_number):
    new_phone_number = str(phone_number)
    if phone_number[0] == '9' and phone_number[1] == '8':
        if phone_number[2] == '0' :
            new_phone_number = phone_number.replace('0','',1)
    else:
        new_phone_number = '0' + '0' + phone_number
    return new_phone_number

# Should compare name with a dictioanary
def validate_name(name):
    for n in Prohibited_name:
        if name == n:
            return True
    return False


def validate_socailaddress(account):
    new_account = str(account)
    if account[0] == '@':
        new_account = account.replace('@','',1)
    return new_account


def locate_ip(ip):
    r = requests.get('http://ip-api.com/json/{}'.format(ip)).json()
    country = None
    if r['status'] == "success":
        country = r["country"]
    return country
    

def generate_slug():
    return ''.join(str(random.choice(string.ascii_uppercase + string.ascii_lowercase)) for _ in range(8))


def send_chat_notification(user,type_notif):
    try:
        fcm = FCMDevice.objects.filter(user=user)
        if type_notif == 1 :
            for i in fcm:
                header = {
                    'Content-Type'  : 'application/json',
                    'Authorization' : 'key=AAAA6996axw:APA91bFlpMzzDLWtxzPGyo7LAL8JVxSQ8MDt8J1cZP5FQixZ3RME_58tb1eQloxcxeFclClmvS8Y2SkOr5IAmUhzXl33joz9-hvfPzsSm_CqveSKcoDgfvyAomYRcaIjCfkgdcmOcfQ8'}
                data = {
                    "notification": {
                        "title": "بیلیگ",
                        "body": "شما پیام جدید دارید",
                        "click_action": "https://billlig.com/profile/inbox",
                        "icon": "https://billlig.com/dstatic//media/images/profile_picture/2020/11/0.png"
                        },
                    "to": i.registration_id
                    }
                r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=header)
        else:
            for i in fcm:
                header = {
                    'Content-Type'  : 'application/json',
                    'Authorization' : 'key=AAAA6996axw:APA91bFlpMzzDLWtxzPGyo7LAL8JVxSQ8MDt8J1cZP5FQixZ3RME_58tb1eQloxcxeFclClmvS8Y2SkOr5IAmUhzXl33joz9-hvfPzsSm_CqveSKcoDgfvyAomYRcaIjCfkgdcmOcfQ8'}
                data = {
                    "notification": {
                        "title": "بیلیگ",
                        "body": "وضعیت پیشنهاد شما تغییر کرد",
                        "click_action": "https://billlig.com/profile/inbox",
                        "icon": "https://billlig.com/dstatic//media/images/profile_picture/2020/11/0.png"
                        },
                    "to": i.registration_id
                    }
                r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=header)

    except FCMDevice.DoesNotExist:
        raise NotFound



    
