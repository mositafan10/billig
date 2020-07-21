import json

from .serializers import MassageSerializer, ConversationSerializer
from .models import Massage, Conversation
from account.models import User

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse

from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view, permission_classes, parser_classes



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_id(request):
    user = User.objects.get(pk=request.user.id)
    receiver = request.data.get("receiver")
    chats = Conversation.objects.all()
    print(chats)
    serializer = ConversationSerializer(chats)
    if chats is not None:
        print("exist")
        return JsonResponse(serializer.data)
    else:
        print("new")
        new_chat = Conversation(receiver=receiver, sender=user)
        new_chat.save()
        return JsonResponse({"id": new_chat.chat_id})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def chat_list(request):
    user = User.objects.get(pk=request.user.id)
    chats = Conversation.objects.all()
    print(chats)
    serializer = ConversationSerializer(chats, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def massage_list(request, chatid):
    massages = Massage.objects.filter(chat_id=chatid)
    serializer = MassageSerializer(massages, many=True)
    return JsonResponse(serializer.data, safe=False)
    
    