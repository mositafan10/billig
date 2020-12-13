from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination, CursorPagination
from fcm_django.models import FCMDevice
from datetime import datetime
import json

from .models import Massage, Conversation
from .serializers import MassageSerializer, ConversationSerializer, ConversationDeserializer, MassageDeserializer
from account.models import User
from advertise.models import Offer
from core.utils import send_chat_notification


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def chat_list(request):
    user = User.objects.get(pk=request.user.id)
    chats = Conversation.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('updated_at')
    for chat in chats:
        counter = Massage.objects.filter(chat_id=chat, is_seen=False).exclude(owner=user).count()
        chat.not_seen = counter
        chat.save()
    chats1 = chats.order_by('-updated_at')
    serializer = ConversationSerializer(chats1, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def massage_list(request, chatid):
    user = User.objects.get(pk=request.user.id)
    massages = Massage.objects.filter(chat_id=chatid).order_by('-create_at') 
    for massage in massages:
        if massage.owner != user and massage.is_seen == False:
            massage.is_seen = True
            massage.save()
    paginator = PageNumberPagination()
    paginator.page_size = request.GET.get('count',20)
    result_page = paginator.paginate_queryset(massages, request)
    serializer = MassageSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_conversation(request):
    offer = Offer.objects.get(slug=request.data.get('offer'))
    conversation, is_created = Conversation.objects.get_or_create(
        slug=offer.slug,
        sender=offer.travel.owner,
        receiver=offer.packet.owner
        )
    if offer.description != "" and is_created :
        Massage.objects.create(owner=conversation.sender, text=offer.description, first_day=True, chat_id=conversation )
    return JsonResponse({"id":conversation.slug})


@api_view(['GET','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def conversation(request, slug):
    conversation = Conversation.objects.get(slug=slug)
    if request.method == 'GET':
        serializer = ConversationSerializer(conversation)
        return JsonResponse(serializer.data)
    elif request.method == 'DELETE':
        conversation.delete()
        return HttpResponse(status=204)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_massage(request, chatid):
    conversation = Conversation.objects.get(slug=chatid)
    if conversation.is_active:
        user = User.objects.get(pk=request.user.id)
        receiver = conversation.receiver
        if user == receiver:
            receiver = conversation.sender
        data = request.data
        if request.FILES.get('billig') != None:
            newdoc = Massage(picture=request.FILES.get('billig'), owner=user, chat_id=conversation)
            newdoc.save()
            try:
                send_chat_notification(receiver, 1)
            except:
                pass
            return HttpResponse(status=200)
        else :
            serializer = MassageDeserializer(data=data)
            if serializer.is_valid():
                serializer.save(owner=user, chat_id=conversation)
                try:
                    send_chat_notification(receiver, 1)
                except:
                    pass
                return JsonResponse(serializer.data, safe=False)
            return JsonResponse(serializer.errors, status=400)
    else:
        raise PermissionDenied(detail=_("این چت امکان دریافت پیام ندارد"))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_lastlogin(request):
    user = User.objects.get(pk=request.user.id)
    return JsonResponse(user.last_login, safe=False)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def notification_register(request):
    token = request.data.get('token','')
    user = User.objects.get(pk=request.user.id)
    data = {
        "registration_id":token,
        "user":user
    }
    fcm = FCMDevice.objects.get_or_create(**data)
    return HttpResponse(status=201)




