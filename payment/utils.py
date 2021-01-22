import json

import requests
from advertise.models import Travel
from Basteh.settings import vandar_mobile, vandar_password
from django.http import HttpResponse, JsonResponse


def pay_to_traveler(user, amount, travel, account_number, slug):
    travel = travel
    number = "IR"+(account_number)
    data = {
        "mobile": vandar_mobile,
        "password": vandar_password,
    }
    r = requests.post('https://api.vandar.io/v2/login', data=data).json()
    token = r['data']['token']
    header = {
        'Authorization' : 'Bearer {}'.format(token)
    }

    data1 = {
        "amount": amount,
        "iban": number,
        "track_id": travel.slug,
    }
    
    r = requests.post('https://api.vandar.io/v2.1/business/billlig/settlement/store', data=data1, headers=header).json()
    if r['status'] == 1:
        # travel.status = 6
        # travel.save()
        # transaction = r['data']
        # transaction = r['data']['settlement']
        transaction = r['data']['settlement'][0]['transaction_id']
        result = {"status":True,"transaction_id":transaction}
        return result
    else:
        # travel.status = 7
        # travel.save()
        return False
        

    