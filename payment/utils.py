from advertise.models import Travel
import requests

def pay_to_traveler(user, amount, payment_number, account_number):
    business = "Billlig"
    travel = Travel.objects.get(slug=payment_number)
    data = {
        "amount": amount,
        "iban": account_number,
        "payment_number": payment_number
    }
    r = requests.post('https://api.vandar.io/v2.1/business/{}/settlement/store'.format(business), data=data).json()
    if r['status'] == 1:
        travel.status = 6
        travel.save()
        return True
    else:
        travel.status = 7
        travel.save()
        return False
        

    