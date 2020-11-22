import json

from .serializers import MassageSerializer, ConversationSerializer, ConversationDeserializer, MassageDeserializer
from .models import Massage, Conversation
from account.models import User
from advertise.models import Offer

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.pagination import PageNumberPagination


from datetime import datetime

from fcm_django.models import FCMDevice

from .notification import send_chat_notification



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
    for chat in chats:
        counter = Massage.objects.filter(chat_id=chat, is_seen=False).exclude(owner=user).count()
        chat.not_seen = counter
        chat.save()
    serializer = ConversationSerializer(chats, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def massage_list(request, chatid):
    user = User.objects.get(pk=request.user.id)
    massages = Massage.objects.filter(chat_id=chatid).order_by('create_at') 
    for massage in massages:
        if massage.owner != user and massage.is_seen == False:
            massage.is_seen = True
            massage.save()
    serializer = MassageSerializer(massages, many=True)
    return JsonResponse(serializer.data, safe=False)
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_conversation(request):
    sender = User.objects.get(pk=request.user.id)
    offer = Offer.objects.get(slug=request.data.get('offer'))
    receiver = User.objects.get(slug=request.data.get('receiver'))
    conversation, is_created = Conversation.objects.get_or_create(offer=offer)
    if offer.description != "" and is_created :
        massage = Massage.objects.create(owner=conversation.sender, text=offer.description, first_day=True, chat_id=conversation )
        massage.save()
    return JsonResponse({"id":conversation.slug})


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
    conversation = Conversation.objects.get(slug=chatid)
    receiver = conversation.receiver
    if user == receiver:
        receiver = conversation.sender
    data = request.data
    if request.FILES.get('billig') != None:
        newdoc = Massage(picture = request.FILES.get('billig'), owner=user, chat_id=conversation)
        newdoc.save()
        # send_chat_notification(receiver)
        return HttpResponse(status=200)
    else :
        serializer = MassageDeserializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=user, chat_id=conversation)
            # send_chat_notification(receiver)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_lastlogin(request):
    user = User.objects.get(pk=request.user.id)
    return JsonResponse(user.last_login, safe=False)


@api_view(['POST'])
def notification_register(request):
    token = request.data.get('token','')
    user = User.objects.get(pk=request.user.id)
    # device = request.headers['user-agent']
    data = {
        "registration_id":token,
        "user":user
    }
    fcm = FCMDevice.objects.get_or_create(**data)
    return HttpResponse(status=201)




