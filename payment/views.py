from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from account.models import User, Profile
from advertise.models import Offer
from .models import TransactionReceive
from .serializer import TransactionReceiveSerializer

from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

import requests

api_key = "f0261280cdc145b4e1e2a7c23a8088d0901ca8c4"
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
        return JsonResponse(r['errors'], status=400, safe=False)


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
    iban = Profile.objects.get(user=user).account_number
    amount = request.data.get('amount')
    payment_number = request.data.get('payment_number')
    data = {
        "amount": amount,
        "iban": iban,
        "payment_number": payment_number
    }
    r = requests.post('https://api.vandar.io/v2.1/business/{business}/settlement/store', data=data).json()
    print(r)
    if r['status'] == 1:
        offer = Offer.objects.get(slug=payment_number)
        travel = offer.travel
        data = {
            "user" : user,
            "travel": travel,
            "amount" : r['amount'],
            "status": True
        }
        transaction = TransactionSend.objects.create(**data) 
        transaction.save()
        return JsonResponse(r, safe=False)
    else:
        return JsonResponse(r, status=400 ,safe=False)

    
