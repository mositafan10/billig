from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from account.models import User, Profile
from advertise.models import Travel, Offer
from .models import TransactionReceive, TransactionSend 
from .serializer import TransactionReceiveSerializer

from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

import requests, json
from Basteh.settings import vandar_api

api_key  = vandar_api
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
    if r['status'] == 1:
        return JsonResponse(r, safe=False)
    else :
        return JsonResponse(r, safe=False, status=400)


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
        offer.status = 3
        offer.save()
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
        serializer = TransactionReceiveSerializer(transaction)
        return JsonResponse(serializer.data)
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
    amount = request.data.get('amount')
    payment_number = request.data.get('payment_number')
    travel = Travel.objects.get(slug=payment_number)
    data = {
        "user" : user,
        "travel": travel,
        "amount" : amount
    }
    travel.status = 8
    travel.save()
    transaction = TransactionSend.objects.create(**data)
    transaction.save()
    return HttpResponse(status=201)
    
    
