from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render

from account.models import User 
from advertise.models import Travel, Offer
from .models import TransactionReceive, TransactionSend , Bank
from .serializer import TransactionReceiveSerializer, BankSerializer

from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound

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
@permission_classes([AllowAny])
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
            "cardNumber": r['cardNumber'],
            "paymentDate": r['paymentDate'],
            "packet": packet,
            "factorNumber": factorNumber,
            "status" : True
        }
        transaction = TransactionReceive.objects.create(**data) 
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
    bank = Bank.objects.get(slug=request.data.get('account'))
    travel = Travel.objects.get(slug=request.data.get('travel'))
    data = {
        "user" : user,
        "travel": travel,
        "amount" : amount,
        "bank": bank
    }
    travel.status = 8
    travel.save()
    transaction = TransactionSend.objects.create(**data)
    transaction.save()
    return HttpResponse(status=201)
    
    

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def accounts(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=request.user.id)
            bank = Bank.objects.filter(user=user)
            serializer = BankSerializer(bank, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Bank.DoesNotExist:
            raise NotFound(detail=_("اطلاعات حساب خود را وارد نمایید"))
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        data = request.data
        serializer = BankSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    
