from django.http import JsonResponse, HttpRequest
from django.db.models import Q
from django.shortcuts import HttpResponse
from django.core.cache import cache
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from datetime import timedelta, datetime

from rest_framework import status, permissions
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotAcceptable, NotFound, PermissionDenied
from rest_framework.pagination import PageNumberPagination

from account.models import User, Country, City, Profile
from core.constant import Expire_Date_Billlig

from .models import Packet, Travel, Offer, Bookmark, Report, PacketPicture
from .utils import send_to_chat
from .serializers import *
from .permissions import IsOwnerPacketOrReadOnly

import json

@api_view(['GET'])
@permission_classes([AllowAny])
def packet_list(request, country):
    # Send just last month orders ( one month expiration policy )
    # The Order should be recheck ( updated_at instead of create_at ) TODO
    packet = Packet.objects.all().filter(create_at__gte=datetime.now()-timedelta(days=Expire_Date_Billlig)).exclude(Q(status='8') | Q(status='9') | Q(status='10') | Q(status='11')).order_by('-create_at')
    # Filter orders Based Country
    if (country == "all"):
        country_packet = packet
    else:
        try:
            request_country = Country.objects.get(eng_name=country)
            country_packet = packet.filter(Q(origin_country=request_country) | Q(destination_country=request_country))
        except Country.DoesNotExist:
            raise NotFound
    paginator = PageNumberPagination()
    paginator.page_size = 12
    result_page = paginator.paginate_queryset(country_packet, request)
    serializer = PacketSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def packet_add(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    buy = request.data.get('buy')
    data = request.data
    serializer = PacketDeserializer(data=data)
    if serializer.is_valid():
        if buy:
            link = request.data.get('link')
            price = request.data.get('price')
            data1 = {
                "link" : link,
                "price" : price,
            }
            serializer1 = BuyinfoSerializer(data=data1)
            if serializer1.is_valid():  
                packet = serializer.save(owner=user)
                serializer1.save(packet=packet)
                return JsonResponse([serializer.data, serializer1.data], status=201, safe=False)
            return JsonResponse(serializer1.errors, status=400)
        else:
            serializer.save(owner=user)
        profile.billlig_done += 1
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def packet_list_user(request):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.filter(owner=user).exclude(status=8).order_by('-create_at')
    serializer = PacketSerializer(packet, many=True)
    return JsonResponse(serializer.data, safe=False)


@permission_classes([AllowAny, IsAuthenticated])
@api_view(['PUT','DELETE','GET'])
def packet_edit(request, slug):
    try:
        packet = Packet.objects.get(slug=slug)
    except Packet.DoesNotExist:
        raise NotFound
    if request.method == 'GET':
        # A repeted user should be removed by cache TODO
        packet.visit_count += 1
        packet.save()
        serilaizer = PacketSerializer(packet)
        return JsonResponse(serilaizer.data, safe=False)
    # TODO change permission to owner   
    if request.method == 'PUT' and IsAuthenticated: 
        data = request.data
        serializer = PacketSerializer1(data=data)
        if serializer.is_valid():
            packet.title = request.data.get('title')
            packet.origin_country = Country.objects.get(id=request.data.get('origin_country'))
            packet.origin_city = City.objects.get(id=request.data.get('origin_city'))
            packet.destination_country = Country.objects.get(id=request.data.get('destination_country'))
            packet.destination_city = City.objects.get(id=request.data.get('destination_city'))
            packet.category = Category.objects.get(pk=request.data.get('category'))
            packet.weight = request.data.get('weight')
            packet.dimension = request.data.get('dimension')
            packet.suggested_price = request.data.get('suggested_price')
            packet.buy = request.data.get('buy')
            packet.description = request.data.get('description')
            packet.phonenumber_visible = request.data.get('phonenumber_visible')
            packet.no_matter_origin = request.data.get('no_matter_origin')
            if request.data.get('buy'):
                link = request.data.get('parcel_link')
                price = request.data.get('parcel_price')
                try:
                    info = Buyinfo.objects.get(packet=packet)
                    info.link = link
                    info.price = price
                except:
                    info = Buyinfo.objects.create(packet=packet, price=price, link=link)
                info.save()
            packet.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    # Change permission to owner TODO 
    elif request.method == 'DELETE' and IsAuthenticated:
        # Should check due to bussiness TODO
        if packet.status == 3 or packet.status == 4 or packet.status == 5 or packet.status == 6 :
            raise PermissionDenied(detail=_("با توجه به وضعیت آگهی امکان حذف آن وجود ندارد"))
        else:
            # We can here delete the packet for ever TODO
            packet.status = '8'
            packet.save()
            return HttpResponse(status=204)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def travel_add(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    flight_date_end = request.data.get("flight_date_end")
    flight_date_start = request.data.get("flight_date_start")
    departure = Country.objects.get(pk=request.data.get("departure"))
    departure_city = City.objects.get(pk=request.data.get("departure_city"))
    destination = Country.objects.get(pk=request.data.get("destination"))
    destination_city = City.objects.get(pk=request.data.get("destination_city"))
    data = request.data
    serializer = TravelSerializer(data=data)
    if serializer.is_valid():
        serializer.save(owner=user)
        # Add double journey
        if flight_date_end != None:
            Travel.objects.create(
                owner=user,
                flight_date_start=flight_date_end,
                departure=destination,
                departure_city=destination_city,
                destination=departure,
                destination_city=departure_city
                )
        profile.travel_done += 1
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
   
        
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def travel_user_list(request):
    user = User.objects.get(pk=request.user.id)
    travel = Travel.objects.filter(owner=user).exclude(status=5).order_by('-create_at')
    serializer = TravelDeserializer(travel, many=True)
    return JsonResponse(serializer.data, safe=False)
    

# permission should be test => if ok then deploy on packet-detail and packet update TODO
@permission_classes([IsOwnerPacketOrReadOnly])
@api_view(['PUT','DELETE'])
def travel_detail(request, pk):
    try:
        travel = Travel.objects.get(slug=pk)
    except Travel.DoesNotExist:
        raise NotFound
    if request.method == 'PUT':
        user = User.objects.get(pk=request.user.id)
        data = request.data
        serializer = TravelSerializer(data=data)
        if serializer.is_valid():
            travel.departure = Country.objects.get(pk=request.data.get('departure'))
            travel.departure_city = City.objects.get(pk=request.data.get('departure_city'))
            travel.destination = Country.objects.get(pk=request.data.get('destination'))
            travel.destination_city = City.objects.get(pk=request.data.get('destination_city'))
            travel.flight_date_start = request.data.get('flight_date_start')
            travel.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        # here should be check that a travel can be deleted or not ? TODO
        # when travel could be deleted then the all its offers should be deleted
        offers = travel.travel_ads.filter()
        for offer in offers :
            offer.delete()
        travel.delete()
        return HttpResponse(status=204)


@permission_classes([IsAuthenticated])
@api_view(['DELETE', 'GET'])
def bookmark(request, slug):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.get(slug=slug)
    if request.method == 'GET':
        try:
            bookmark = Bookmark.objects.get(owner=user, packet=packet)
            return JsonResponse({"bookmark":True})
        except Bookmark.DoesNotExist:
            return JsonResponse({"bookmark":False})
    if request.method == 'DELETE':
        try:
            bookmark = Bookmark.objects.get(owner=user, packet=packet)
            bookmark.delete()
            return HttpResponse(status=204)
        except Bookmark.DoesNotExist:
            raise NotFound(detail=_("آگهی مورد نظر پیدا نشد"))
        

@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def bookmark_list(request):
    user = User.objects.get(pk=request.user.id)
    if request.method ==  'GET':
        bookmark = Bookmark.objects.filter(owner=user)
        serializer = BookmarkDeserializer(bookmark, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        packet = Packet.objects.get(slug=request.data.get('packet'))
        # check for owner of bookmark
        if packet.owner != user :
            bookmark = Bookmark.objects.filter(owner=user, packet=packet)
            # check for whether the user bookmark this packet before or not 
            if bookmark.count() == 0 :
                data = {
                    "packet": packet.id
                }
                serializer = BookmarkSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(owner=user)
                    return JsonResponse(serializer.data, status=201)
                return JsonResponse(serializer.errors, status=400)
            else:
                bookmark.delete()
                return HttpResponse(status=204)
        else:
            detail = _("! این آگهی برای خودتان است")
            raise NotAcceptable(detail) # is this error correct ? TODO


# List of packet's offers
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def offer_list(request, slug):
    try:
        packet = Packet.objects.get(slug=slug)
    except Packet.DoesNotExist:
        raise NotFound
    offer = Offer.objects.filter(packet=packet).exclude(status="7").exclude(status="8").order_by('-create_at')
    serializer = OfferSerializer(offer, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def offer(request):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.get(slug=request.data.get("packet"))
    travel = Travel.objects.get(slug=request.data.get("travel"))
    # between which of offers we should serach ? TODO
    # should be used "get" instead "filter" because there is just on offer between on packet and one travel. TODO
    offer    = Offer.objects.filter(travel=travel, packet=packet).exclude(status=8)
    if offer.count() == 0 :
        if packet.owner != user :
            data = request.data
            serializer = OfferDeserializer(data=data)
            if serializer.is_valid():
                serializer.save(packet=packet, travel=travel)
                # can we increase offer_count of travel and packet here ? TODO ( I think yes : after save offer it can)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        else:
            detail = _("این آگهی برای خودتان است!")
            raise NotAcceptable(detail)
    else:
        detail=_("قبلا برای این اگهی پیشنهاد گذاشته‌اید.")
        raise NotAcceptable(detail)
    

# This should be update just by two user : traveler and billliger.
# So we need a custom permission here not is_authenticated TODO
# Should edit url and insert slug into it not in body TODO
# Should write with try/expection not by if TODO
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def offer_update(request):
    slug = request.data.get('slug')
    offer = Offer.objects.get(slug=slug)
    if (request.data.get('price')):
        price = request.data.get('price')
        offer.price = price
    if (request.data.get('status')):
        status = request.data.get('status')
        offer.status = status
        if(status == 8):
            offer.delete()
    if (request.data.get('parcelPrice')):
        parcelPrice = request.data.get('parcelPrice')
        offer.parcelPrice = parcelPrice
    offer.save()
    return HttpResponse(status=200)


@permission_classes([IsOwnerPacketOrReadOnly])
@api_view(['DELETE'])
def offer_delete(request, slug):
    try:
        offer = Offer.objects.get(slug=slug)
    except Offer.DoesNotExist:
        raise NotFound
    offer.delete()
    # offer.packet.offer_count -= 1
    # offer.packet.save()
    # offer.travel.offer_count -= 1
    # offer.travel.save()
    return HttpResponse(status=204)


@permission_classes([AllowAny])        
@api_view(['GET'])
def get_picture(request, slug):
    # Defualt picture 
    if slug == '1':
        picture = PacketPicture.objects.get(pk=1)
        serializer = PictureSerializer(picture)
        return JsonResponse(serializer.data, safe=False)
    else:
        picture = PacketPicture.objects.get(slug=slug)
        serializer = PictureSerializer(picture)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])        
def get_user_offer(request):
    user = User.objects.get(pk=request.user.id)
    offer = Offer.objects.filter(travel__owner=user).exclude(status=8).order_by('-updated_at')
    serializer = OfferSerializer(offer, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([AllowAny])  
def category_list(request, level):
    categories = Category.objects.filter(is_active=True, level=level)
    serializer = CategorySerializer(categories, many=True)
    return JsonResponse(serializer.data, safe=False)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_file(request):
    newdoc = PacketPicture(image_file = request.FILES.get('billig'))
    newdoc.save() 
    return JsonResponse({"id": newdoc.slug})