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
from core.utils import send_chat_notification

from .models import *
from .serializers import *
from .utils import send_to_chat
from .permissions import IsOwnerPacketOrReadOnly

import json

@api_view(['GET'])
@permission_classes([AllowAny])
def packet_list(request, country, category):
    # Send just last month orders ( one month expiration policy )
    packet = Packet.objects.all().filter(create_at__gte=datetime.now()-timedelta(days=Expire_Date_Billlig)).filter(Q(status='0') | Q(status='1') | Q(status='3')).order_by('-create_at')
    filter_packets = packet

    # Filter orders Based Country
    if (country == "all"):
        filter_packets = filter_packets
    else:
        try:
            request_country = Country.objects.get(eng_name=country)
            filter_packets = packet.filter(Q(origin_country=request_country) | Q(destination_country=request_country))
        except Country.DoesNotExist:
            pass
    if (Category == "all"):
        filter_packets = filter_packets
    else:
        try:
            request_category = Category.objects.get(eng_name=category)
            filter_packets = filter_packets.filter(category=request_category)
        except Category.DoesNotExist:
            pass
    paginator = PageNumberPagination()
    paginator.page_size = 12
    result_page = paginator.paginate_queryset(filter_packets, request)
    serializer = PacketSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def packet_add(request):
    user = User.objects.get(pk=request.user.id)
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
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def packet_list_user(request):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.filter(owner=user).exclude(status=8).exclude(status=7).order_by('-create_at')
    serializer = PacketSerializer(packet, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def packet_list_user_completed(request):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.filter(owner=user, status=7).exclude(status=8).order_by('-create_at')
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
    user = User.objects.get(pk=request.user.id)
    if user == packet.owner:
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
                packet.save()
                if request.data.get('buy'):
                    link = request.data.get('parcel_link')
                    price = request.data.get('parcel_price')
                    slug = packet.packet_info.get().slug
                    salam = Buyinfo.objects.get(slug=slug)
                    buyinfo, is_created = Buyinfo.objects.update_or_create(
                        packet=packet, slug=packet.packet_info.get().slug,
                        defaults={'price': price, 'link': link, 'packet': packet}
                        )
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        elif request.method == 'DELETE' and IsAuthenticated:
            packet.status = 8
            packet.save()
            return HttpResponse(status=204)
    else:
        raise PermissionDenied(detail=_("انجام این عملیات برای شما ممکن نیست"))
        

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
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
   
        
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def travel_user_list(request):
    user = User.objects.get(pk=request.user.id)
    travel = Travel.objects.filter(owner=user).filter(Q(status=0) | Q(status=1) | Q(status=2) | Q(status=3)).order_by('-create_at')
    serializer = TravelDeserializer(travel, many=True)
    return JsonResponse(serializer.data, safe=False)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def travel_user_list_completed(request):
    user = User.objects.get(pk=request.user.id)
    travel = Travel.objects.filter(owner=user).filter(Q(status=4) | Q(status=6) | Q(status=7) | Q(status=8)).order_by('-create_at')
    serializer = TravelDeserializer(travel, many=True)
    return JsonResponse(serializer.data, safe=False)
    

@permission_classes([IsAuthenticated])
@api_view(['PUT','DELETE','GET'])
def travel_detail(request, pk):
    try:
        travel = Travel.objects.get(slug=pk)
    except Travel.DoesNotExist:
        raise NotFound
    user = User.objects.get(pk=request.user.id)
    if user == travel.owner:
        # For travel edit
        if request.method == 'GET':
            serializer = TravelDeserializer(travel)
            return JsonResponse(serializer.data)
        if request.method == 'PUT':
            if travel.status == 2 :
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
            else:
                raise PermissionDenied(detail=_("امکان ویرایش این سفر وجود ندارد"))
        elif request.method == 'DELETE':
            if travel.status == 0 or travel.status == 2:
                travel.status = 5
                travel.save()
                return HttpResponse(status=204)
            else:
                raise PermissionDenied(detail=_("امکان حذف این سفر وجود ندارد"))
    else:
        raise PermissionDenied(detail=_("انجام این عملیات برای شما ممکن نیست"))


@permission_classes([IsAuthenticated])
@api_view(['DELETE', 'GET'])
def bookmark(request, slug):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.get(slug=slug)
    if request.method == 'GET':
        if Bookmark.objects.filter(owner=user, packet=packet).exists():
            return JsonResponse({"bookmark":True})
        else:
            return JsonResponse({"bookmark":False})
    if request.method == 'DELETE':
        try:
            bookmark = Bookmark.objects.get(owner=user, packet=packet)
        except Bookmark.DoesNotExist:
            raise NotFound(detail=_("آگهی مورد نظر پیدا نشد"))
        bookmark.delete()
        return HttpResponse(status=204)
        

@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def bookmark_list(request):
    user = User.objects.get(pk=request.user.id)
    if request.method ==  'GET':
        bookmark = Bookmark.objects.filter(owner=user)
        serializer = BookmarkDeserializer(bookmark, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        packet = Packet.objects.select_related("owner").get(slug=request.data.get('packet'))
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
    packet = Packet.objects.select_related("owner").get(slug=request.data.get("packet"))
    travel = Travel.objects.get(slug=request.data.get("travel"))

    # between which of offers we should serach ? TODO
    if Offer.objects.filter(travel=travel, packet=packet).exists() is not True:
        if packet.owner != user :
            data = request.data
            serializer = OfferDeserializer(data=data)
            if serializer.is_valid():
                serializer.save(packet=packet, travel=travel)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        else:
            detail = _("این آگهی برای خودتان است!")
            raise NotAcceptable(detail)
    else:
        detail=_("قبلا برای این اگهی پیشنهاد گذاشته‌اید.")
        raise NotAcceptable(detail)
    

# Should write with try/expection not by if TODO
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def offer_update(request, slug):
    user = User.objects.get(pk=request.user.id)
    try:
        offer = Offer.objects.select_related("packet").get(slug=slug)
        receiver = offer.packet.owner
        if offer.packet.owner == user:
            receiver = offer.travel.owner
    except Offer.DoesNotExist:
        raise NotFound(detail=_("پیشنهاد مورد نظر پیدا نشد"))
    if offer.packet.owner == user or offer.travel.owner == user:
        if (request.data.get('price')):
            offer.price = request.data.get('price')
        if (request.data.get('status')):
            offer.status = request.data.get('status')
        if (request.data.get('parcelPrice')):
            offer.parcelPrice = request.data.get('parcelPrice')
        offer.save()
        try:
            send_chat_notification(receiver, 2)
        except expression as identifier:
            pass
        return HttpResponse(status=200)
    else:
        raise Exception(detail=_("انجام این عملیات این مقدور نیست"))


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def offer_delete(request, slug):
    user = User.objects.get(pk=request.user.id)
    try:
        offer = Offer.objects.get(slug=slug)
    except Offer.DoesNotExist:
        raise NotFound
    if offer.travel.owner == user:
        offer.status = 8
        offer.save()
        return HttpResponse(status=204)
    else:
        raise PermissionDenied(detail=_("امکان حذف توسط شما وجود ندارد"))
    

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
def get_user_offer(request,travel):
    user = User.objects.get(pk=request.user.id)
    offerTravel = Travel.objects.get(slug=travel)
    offer = Offer.objects.filter(travel__owner=user,travel=offerTravel).exclude(status=8).order_by('-updated_at')
    serializer = OfferSerializer(offer, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([AllowAny])  
def category_list(request):
    categories = Category.objects.filter(is_active=True).order_by('name')
    serializer = CategorySerializer(categories, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([AllowAny])  
def subcategory_list(request, category):
    categories = SubCategory.objects.filter(is_active=True, category=category)
    serializer = SubCategorySerializer(categories, many=True)
    return JsonResponse(serializer.data, safe=False)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_file(request):
    newdoc = PacketPicture(image_file = request.FILES.get('billig'))
    newdoc.save() 
    return JsonResponse({"id": newdoc.slug})


@permission_classes([IsOwnerPacketOrReadOnly])
@api_view(['POST'])
def add_remove_reason(request, slug):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.get(slug=slug)
    data = request.data
    serializer = RemoveReasonSerializer(data=data)
    if serializer.is_valid():
        serializer.save(packet=packet)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@permission_classes([IsOwnerPacketOrReadOnly])
@api_view(['POST'])
def add_travel_remove_reason(request, slug):
    user = User.objects.get(pk=request.user.id)
    travel = Travel.objects.get(slug=slug)
    data = request.data
    serializer = TravelRemoveReasonSerializer(data=data)
    if serializer.is_valid():
        serializer.save(travel=travel)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def check_report(request, slug):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.get(slug=slug)
    if Report.objects.filter(owner=user, packet=packet).exists():
        return JsonResponse({"report": True})
    else:
        return JsonResponse({"report": False})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_report(request):
    user = User.objects.get(pk=request.user.id)
    # should be test TODO
    packet = Packet.objects.select_related("owner").get(slug=request.data.get('packet'))
    if user == packet.owner:
        detail = _("این آگهی برای خودتان است")
        return JsonResponse({"detail":detail},status=400)
    data = request.data
    serializer = ReportSerializer(data=data)
    if serializer.is_valid():
        serializer.save(owner=user, packet=packet)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

