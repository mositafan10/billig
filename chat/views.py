import json

from .serializers import MassageSerializer, ConversationSerializer, ConversationDeserializer, MassageDeserializer
from .models import Massage, Conversation
from account.models import User
from advertise.models import Offer

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.db.models import Q

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
    chats = Conversation.objects.filter(Q(sender=user) | Q(receiver=user))
    print(chats)
    serializer = ConversationSerializer(chats, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def massage_list(request, chatid):
    massages = Massage.objects.filter(chat_id=chatid)
    serializer = MassageSerializer(massages, many=True)
    return JsonResponse(serializer.data, safe=False)
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_conversation(request):
    sender = User.objects.get(pk=request.user.id)
    offer_slug = request.data.get('offer')
    offer = Offer.objects.get(slug=offer_slug)
    conversation, is_created = Conversation.objects.get_or_create(offer=offer)
    if is_created:
        data = request.data
        serializer = ConversationDeserializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=sender)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({"id":conversation.id})

   

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_massage(request):
    user = User.objects.get(pk=request.user.id)
    data = request.data
    serializer = MassageDeserializer(data=data)
    if serializer.is_valid():
        serializer.save(owner=user)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse(serializer.errors, status=400)
