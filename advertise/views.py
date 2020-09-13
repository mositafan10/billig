from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import HttpResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Packet, Travel, Offer, Bookmark, Report, PacketPicture
from account.models import User, Country, City
from .serializers import *
from .permissions import IsOwnerPacketOrReadOnly


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def packet_list(request):
    if request.method == 'GET':
        packet = Packet.objects.all().exclude(Q(status='8') | Q(status='9') | Q(status='10') | Q(status='11')).order_by('-create_at')
        serializer = PacketSerializer(packet, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        data = request.data
        serializer = PacketDeserializer(data=data)
        buy = request.data.get('buy')
        if serializer.is_valid():
            serializer.save(owner=user)
            if buy:
                link = request.data.get('link')
                price = request.data.get('price')
                data1 = {
                    "link" : link,
                    "price" : price,
                    "packet": serializer
                }
                serializer1 = BuyinfoSerializer(data=data1)
                if serializer1.is_valid():
                    serializer1.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def packet_list_user(request):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.filter(owner=user).order_by('-create_at')
    serializer = PacketSerializer(packet, many=True)
    return JsonResponse(serializer.data, safe=False)


@permission_classes([AllowAny])
@api_view(['GET'])
def user_packet_list(request):
    if request.method == 'GET':
        packet = Packet.objects.all()
        serializer = PacketSerializer(packet, many=True)
        return JsonResponse(serializer.data)


@permission_classes([AllowAny])
@api_view(['GET', 'PUT', 'DELETE'])
def packet_detail(request, slug):
    try:
        packet = Packet.objects.get(slug=slug)
    except Packet.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serilaizer = PacketSerializer(packet)
        return JsonResponse(serilaizer.data, safe=False)
    elif request.method == 'PUT':
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
            packet.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        packet.status = '8'
        packet.save()
        return HttpResponse(status=204)


@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def travel_add(request):
    user = User.objects.get(pk=request.user.id)
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
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
   
        
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def travel_user_list(request):
    user = User.objects.get(pk=request.user.id)
    travel = Travel.objects.filter(owner=user).order_by('create_at')
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
@api_view(['POST','GET','DELETE'])
def bookmark(request, slug):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.get(slug=slug)
    if request.method == 'GET':
        count = Bookmark.objects.filter(owner=user, advertise=packet).count()
        print(count)
        if (count == 0):
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)
    elif request.method == 'POST':
        data = request.data
        serializer = BookmarkSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=user, advertise=packet)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        bookmark = Bookmark.objects.filter(owner=user, advertise=packet)
        bookmark.delete()
        return HttpResponse(status=204)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def bookmark_list(request):
    user = User.objects.get(pk=request.user.id)
    bookmark = Bookmark.objects.filter(owner=user)
    serializer = BookmarkDeserializer(bookmark, many=True)
    return JsonResponse(serializer.data, safe=False)


@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@api_view(['POST'])
def upload_file(request):
    newdoc = PacketPicture(image_file = request.FILES.get('billig'))
    newdoc.save() 
    return JsonResponse({"id": newdoc.id})


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
@parser_classes([MultiPartParser, FormParser, JSONParser])
def offer(request):
    slug = request.data.get("slug")
    packet = Packet.objects.get(slug=request.data.get("packet"))
    price = request.data.get("price")
    description = request.data.get("description")
    travel_slug = request.data.get("travel")
    travel = Travel.objects.get(slug=travel_slug)
    data = request.data
    serializer = OfferDeserializer(data=data)
    if serializer.is_valid():
        serializer.save(packet=packet, travel=travel)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

  
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # TODO is need owner of object
def offer_update(request):
    slug = request.data.get('slug')
    offer = Offer.objects.get(slug=slug)
    if (request.data.get('price')):
        price = request.data.get('price')
        offer.price = price
        offer.save()
    if (request.data.get('status')):
        status = request.data.get('status')
        offer.status = status
        offer.save()
        if(status == 8):
            offer.packet.offer_count -= 1
            offer.save()
    
    return HttpResponse(status=200)

@permission_classes([AllowAny])        
@api_view(['GET'])
def get_picture(request, pk):
    picture = PacketPicture.objects.get(pk=pk)
    serializer = PictureSerializer(picture)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])        
def get_user_offer(request):
    user = User.objects.get(pk=request.user.id)
    offer = Offer.objects.filter(travel__owner=user)
    serializer = OfferSerializer(offer, many=True)
    return JsonResponse(serializer.data, safe=False)

