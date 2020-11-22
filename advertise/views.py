from django.http import JsonResponse, HttpRequest
from django.db.models import Q
from django.shortcuts import HttpResponse
from django.core.cache import cache
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

from rest_framework import status, permissions
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import MethodNotAllowed, NotAcceptable, NotFound, PermissionDenied
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from account.models import User, Country, City, Profile

from .models import Packet, Travel, Offer, Bookmark, Report, PacketPicture
from .serializers import *
from .permissions import IsOwnerPacketOrReadOnly

import json

@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def packet_list(request, country):
    packet = Packet.objects.all().exclude(Q(status='8') | Q(status='9') | Q(status='10') | Q(status='11')).order_by('-create_at')
    if (country == "all"):
        country_packet = packet
    else:
        try:
            request_country =  Country.objects.get(eng_name=country)
            country_packet = packet.filter(Q(origin_country=request_country) | Q(destination_country=request_country))
        except:
            raise NotFound(detail=_("Country Not Found"))
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
        packet_id = serializer.save(owner=user)
        if buy:
            link = request.data.get('link')
            price = request.data.get('price')
            data1 = {
                "link" : link,
                "price" : price,
                "packet": packet_id.id
            }
            serializer1 = BuyinfoSerializer(data=data1)
            if serializer1.is_valid():  
                serializer1.save()
                return JsonResponse([serializer.data, serializer1.data], status=201, safe=False)
            return JsonResponse(serializer1.errors, status=400)
        return JsonResponse(serializer.data, status=201)
        profile.billig_done += 1
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def packet_list_user(request):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.filter(owner=user).exclude(status=8).order_by('-create_at')
    serializer = PacketSerializer(packet, many=True)
    return JsonResponse(serializer.data, safe=False)


@permission_classes([AllowAny])
@api_view(['GET'])
def user_packet_list(request):
    if request.method == 'GET':
        packet = Packet.objects.all()
        serializer = PacketSerializer(packet, many=True)
        return JsonResponse(serializer.data)


# @permission_classes([AllowAny])
# @api_view(['GET'])
# def packet_detail(request, slug):
#     try:
#         packet = Packet.objects.get(slug=slug)
#         packet.visit_count += 1
#         packet.save()
#         serilaizer = PacketSerializer(packet)
#         return JsonResponse(serilaizer.data, safe=False)
#     except Packet.DoesNotExist:
#         return HttpResponse(status=404)


@permission_classes([AllowAny, IsAuthenticated])
@api_view(['PUT', 'DELETE','GET'])
def packet_edit(request, slug):
    try:
        packet = Packet.objects.get(slug=slug)
    except Packet.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        packet.visit_count += 1
        packet.save()
        serilaizer = PacketSerializer(packet)
        return JsonResponse(serilaizer.data, safe=False)
    if request.method == 'PUT' and IsAuthenticated: # TODO change permission to owner
        data = request.data
        serializer = PacketSerializer1(data=data)
        if serializer.is_valid():
            packet.title = request.data.get('title')
            packet.origin_country = Country.objects.get(id=request.data.get('origin_country'))
            packet.origin_city = City.objects.get(id=request.data.get('origin_city'))
            packet.destination_country = Country.objects.get(id=request.data.get('destination_country'))
            packet.destination_city = City.objects.get(id=request.data.get('destination_city'))
            packet.category = request.data.get('category')
            packet.weight = request.data.get('weight')
            packet.dimension = request.data.get('dimension')
            packet.suggested_price = request.data.get('suggested_price')
            packet.buy = request.data.get('buy')
            packet.description = request.data.get('description')
            packet.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE' and IsAuthenticated: # TODO change permission to owner
        if packet.status == 3 or packet.status == 4 or packet.status == 5 or packet.status == 6 :
            raise PermissionDenied(detail=_("با توجه به وضعیت آگهی امکان حذف آن وجود ندارد"))
        else:
            packet.status = '8'
            packet.save()
            return HttpResponse(status=204)


@parser_classes([MultiPartParser, FormParser, JSONParser])
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
    travel = Travel.objects.filter(owner=user).order_by('-create_at')
    serializer = TravelDeserializer(travel, many=True)
    return JsonResponse(serializer.data, safe=False)
    

@permission_classes([IsOwnerPacketOrReadOnly])
@api_view(['GET', 'PUT', 'DELETE'])
def travel_detail(request, pk):
    try:
        travel = Travel.objects.get(slug=pk)
    except Travel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = TravelDeserializer(travel)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
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
        travel.delete()
        return HttpResponse(status=204)


@permission_classes([AllowAny])
@api_view(['GET','POST'])
def visit_packet(request, pk):
    try:
        packet = Packet.objects.get(pk=pk)
    except Packet.DoesNotExist:
        return HttpResponse(status=404)
    model_name = "visit_packet"
    ip = request.META.get("HTTP_REMOTE_ADDR")
    key = "%s_%s" % (model_name, ip)
    if not cache.get(key) == pk:
        cache.set(key, pk, 4)
        packet.visit()
        return HttpResponse(status=201)
    return HttpResponse(status=400)


@permission_classes([AllowAny])
@api_view(['GET','POST'])
def visit_travel(request, pk):
    try:
        travel = Travel.objects.get(pk=pk)
    except Travel.DoesNotExist:
        return HttpResponse(status=404)
    travel = Travel.objects.get(pk=pk)
    model_name = "visit_travel"
    ip = request.META.get("HTTP_REMOTE_ADDR")
    key = "%s_%s" % (model_name, ip)
    if not cache.get(key) == pk:
        cache.set(key, pk, 4)
        travel.visit()
        return HttpResponse(status=201)
    return HttpResponse(status=400)


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
            raise NotFound(detail="آگهی مورد نظر پیدا نشد")
        
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
        if packet.owner != user :
            bookmark = Bookmark.objects.filter(owner=user, packet=packet)
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
            detail = "! این آگهی برای خودتان است"
            raise NotAcceptable(detail)



@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@api_view(['POST'])
def upload_file(request):
    http = request.META['REMOTE_ADDR'] 
    newdoc = PacketPicture(image_file = request.FILES.get('billig'))
    newdoc.save() 
    return JsonResponse({"id": newdoc.slug})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def offer_list(request, slug):
    try:
        packet = Packet.objects.get(slug=slug)
    except:
        return HttpResponse(status=404)
    offer = Offer.objects.filter(packet=packet).exclude(status="7").exclude(status="8").order_by('-create_at')
    serializer = OfferSerializer(offer, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def offer(request):
    slug = request.data.get("slug")
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.get(slug=request.data.get("packet"))
    travel = Travel.objects.get(slug=request.data.get("travel"))
    offer = Offer.objects.filter(travel=travel, packet=packet)
    if offer.count() == 0 :
        if packet.owner != user :
            data = request.data
            serializer = OfferDeserializer(data=data)
            if serializer.is_valid():
                serializer.save(packet=packet, travel=travel)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        else:
            detail = "این آگهی برای خودتان است. امکان ثبت پیشنهاد وجود ندارد"
            raise NotAcceptable(detail)
    else:
        raise NotAcceptable(detail="برای هر آگهی فقط یک پیشنهاد مجاز است")
    
  
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
            offer.packet.offer_count -= 1
    if (request.data.get('parcelPrice')):
        parcelPrice = request.data.get('parcelPrice')
        offer.parcelPrice = parcelPrice
    offer.save()
    return HttpResponse(status=200)


@permission_classes([AllowAny])        
@api_view(['GET'])
def get_picture(request, slug):
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

