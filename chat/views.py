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

from datetime import datetime


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_id(request):
    user = User.objects.get(pk=request.user.id)
    receiver = request.data.get("receiver")
    chats = Conversation.objects.all()
    serializer = ConversationSerializer(chats)
    if chats is not None:
        return JsonResponse(serializer.data)
    else:
        new_chat = Conversation(receiver=receiver, sender=user)
        new_chat.save()
        return JsonResponse({"id": new_chat.chat_id})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def chat_list(request):
    user = User.objects.get(pk=request.user.id)
    chats = Conversation.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-updated_at')

    # #for count new massages
    # massages = Massage.objects.filter(chat_id=chatid)
    # last_login = user.last_login
    # last_logout = user.last_logout
    # new_massages_count = massages.filter(create_at__range=(last_logout, last_login )).count()
    # conversation = Conversation.objects.get(id=chatid)

    serializer = ConversationSerializer(chats, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def massage_list(request, chatid):
    user = User.objects.get(pk=request.user.id)
    massages = Massage.objects.filter(chat_id=chatid).order_by('create_at')
    serializer = MassageSerializer(massages, many=True)
    return JsonResponse(serializer.data, safe=False)
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_conversation(request):
    sender = User.objects.get(pk=request.user.id)
    offer_slug = request.data.get('offer')
    offer = Offer.objects.get(slug=offer_slug)
    receiver_id = request.data.get('receiver')
    receiver = User.objects.get(pk=receiver_id)
    conversation, is_created = Conversation.objects.get_or_create(offer=offer, receiver=receiver, sender=sender)
    if conversation.id :
        return JsonResponse({"id":conversation.id})
    else:
        conversation = Conversation.objects.get_or_create(offer=offer, receiver=sender, sender=receiver)
        return JsonResponse({"id":conversation.id})



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def conversation_info(request, pk):
    conversation = Conversation.objects.get(pk=pk)
    serializer = ConversationSerializer(conversation)
    return JsonResponse(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_massage(request, chatid):
    user = User.objects.get(pk=request.user.id)
    conversation = Conversation.objects.get(pk=chatid)
    data = request.data
    if request.FILES.get('billig') != None:
        newdoc = Massage(picture = request.FILES.get('billig'), owner=user, chat_id=conversation)
        newdoc.save()
        return JsonResponse({"id": newdoc.id})
    else :
        serializer = MassageDeserializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=user, chat_id=conversation)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_lastlogin(request):
    user = User.objects.get(pk=request.user.id)
    return JsonResponse(user.last_login, safe=False)