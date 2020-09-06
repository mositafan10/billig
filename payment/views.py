from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from account.models import User
from advertise.models import Offer
from .models import TransactionReceive
from .serializer import TransactionReceiveSerializer

from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated

import requests

api_key = "b44fbd8273bd9988900a64c7b969593b5d004046"
business = "Billlig"

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send(request):
    amount = request.data.get('amount')
    callback_url = request.data.get('callback_url')
    factorNumber = request.data.get('factorNumber')
    data = {
        "api_key": api_key,
        "amount": amount,
        "callback_url": callback_url,
        "factorNumber": factorNumber
    }
    r = requests.post('https://ipg.vandar.io/api/v3/send', data=data).json()
    return JsonResponse(r, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify(request):
    user = User.objects.get(pk=request.user.id)
    token = request.data.get('token')
    data = {
        "api_key": api_key,
        "token" : token
    }
    r = requests.post('https://ipg.vandar.io/api/v3/verify', data=data).json()
    if r['status'] == 1:
        factorNumber = r['factorNumber']
        offer = Offer.objects.get(slug=factorNumber)
        packet = offer.packet
        data = {
            "user" : user,
            "amount" : r['amount'],
            "transId": r['transId'],
            "packet": packet,
            "factorNumber": factorNumber,
            "status" : True
        }
        transaction = TransactionReceive.objects.create(**data) 
        transaction.save()
        return HttpResponse(status=201)
    else :
        return JsonResponse(r['errors'], safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactions_list(request):
    user = User.objects.get(pk=request.user.id)
    transactions = TransactionReceive.objects.filter(user=user).order_by('-create_at')
    serializer = TransactionReceiveSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_to_traveler(request):
    user = User.objects.get(pk=request.user.id)
    amount = request.data.get('amount')
    iban = request.data.get('iban')
    data = {
        "amount": amount,
        "iban": iban,
    }
    r = requests.post('https://api.vandar.io/v2.1/business/{business}/settlement/store', data=data).json()
    if r['status'] == 1:
        data = {
            "user" : user,
            "amount" : r['amount'],
            "transaction_id": r['transaction_id']
            
        }
