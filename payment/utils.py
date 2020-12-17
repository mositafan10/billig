from advertise.models import Travel
from django.http import JsonResponse, HttpResponse
import requests, json

def pay_to_traveler(user, amount, travel, account_number, slug):
    travel = travel
    number = "IR"+(account_number)
    data = {
        "mobile": "09128161004",
        "password": "Baranbenyamin161191",
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
    print(r)
    if r['status'] == 1:
        travel.status = 6
        travel.save()
        transaction = r['data']
        print(transaction)
        transaction = r['data']['settlement']
        print(transaction)
        transaction = r['data']['settlement'][0]['transaction_id']
        print(transaction)
        result = {"status":True,"transaction_id":transaction}
        print(result)
        return result
    else:
        travel.status = 7
        travel.save()
        return False
        

    