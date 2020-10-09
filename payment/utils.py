import requests
from advertise.models import Travel
# from .models import TransactionSend

def pay_to_traveler(user, amount, payment_number):
    iban = Profile.objects.get(user=user).account_number
    travel = Travel.objects.get(slug=payment_number)
    data = {
        "amount": amount,
        "iban": iban,
        "payment_number": payment_number
    }
    r = requests.post('https://api.vandar.io/v2.1/business/{business}/settlement/store', data=data).json()
    if r['status'] == 1:
        travel.status = 6
        travel.save()
        return True
    else:
        travel.status = 7
        travel.save()
        return False
        

    