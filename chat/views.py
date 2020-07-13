import json

from .serializers import MassageSerializer, ChatIdSerializer
from .models import Massage, ChatID
from account.models import User

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.db.models import Q

from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view, permission_classes, parser_classes



@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def chat_list(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'GET':
        massage = Massage.objects.all()
        serializer = MassageSerializer(massage, many=True,)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        serializer = MassageSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(sender=user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_id(request):
    user = User.objects.get(pk=request.user.id)
    receiver = request.data.get("receiver")
    chats = ChatID.objects.filter(Q(sender=user) | Q(receiver=user))
    print (chats)
    serializer = ChatIdSerializer(chats)
    if chats is not None:
        return JsonResponse(serializer.data)
    else:
        return chats.chat_id
    return JsonResponse(serializer.data, safe=False)