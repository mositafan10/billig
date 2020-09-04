from django.http import JsonResponse, HttpResponse
from account.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view 
import requests
import json


@api_view(['POST'])
def send(request):
    user = User.objects.get(pk=request.user.id)
    api_key = "xxxx"
    amount = request.data.get('amount')
    callback_url = request.data.get('callback_url')
    # mobile_number = user.phone_number # what about foreign number
    data = {
        "api_key": api_key,
        "amount": amount,
        "callback_url": callback_url,
    }

    # request = requests.post('https://ipg.vandar.io/api/v3/send', data=data)
    # print(request.content)
    return HttpResponse(status=200)
    # return json(request.content, safe=False)

# @api_view(['POST'])
# def verify(requests):
