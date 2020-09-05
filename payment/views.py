from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from account.models import User
from .models import TransactionReceive
from .serializer import TransactionReceiveSerializer

from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated

import requests

api_key = "xxxx"

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send(request):
    amount = request.data.get('amount')
    callback_url = request.data.get('callback_url')
    data = {
        "api_key": api_key,
        "amount": amount,
        "callback_url": callback_url,
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
        data = {
            "user" : user,
            "amount" : r['amount'],
            "transID": r['transID'],
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
