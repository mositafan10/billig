from fcm_django.models import FCMDevice
from rest_framework.exceptions import NotFound
import requests, json

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