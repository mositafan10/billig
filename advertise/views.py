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
from account.models import User
from .serializers import *
from .permissions import IsOwnerPacketOrReadOnly


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def packet_list(request):
    if request.method == 'GET':
        packet = Packet.objects.filter(Q(status='2') | Q(status='3')).order_by('-create_at')
        serializer = PacketSerializer(packet, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        data = request.data
        serializer = PacketDeserializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def packet_list_user(request):
    user = User.objects.get(pk=request.user.id)
    packet = Packet.objects.filter(owner=user)
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
@api_view(['PUT'])
def update_packet(request, pk):
    if request.method == 'PUT':
        packet = Packet.objects.get(pk=pk)
        if request.user == packet.owner.user :
            data = JSONParser.parse(request)
            serializer = PacketSerializer(data=data)
            if serialzier.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.error, status=400)
        return JsonResponse({"Access Deneid" : "You have not permision to edit this packet"}, status=400)


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
        data = JSONParser.parse(request)
        serializer = PacketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serialzier.errors, status=400)
    elif request.method == 'DELETE':
        packet.delete()
        return HttpResponse(status=204)


@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def travel_add(request):
    user = User.objects.get(pk=request.user.id)
    data = request.data
    serializer = TravelSerializer(data=data)
    if serializer.is_valid():
        serializer.save(owner=user)
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def travel_user_list(request):
    user = User.objects.get(pk=request.user.id)
    travel = Travel.objects.filter(owner=user)
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
        data = JSONParser.parse(request)
        serializer = TravelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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
    packet = Packet.objects.get(pk=pk)
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


@permission_classes([AllowAny])
@api_view(['GET','POST'])
def bookmark(request, pk):
    if request.method == 'POST':
        packet = Packet.objects.get(pk=pk)
        data = JSONParser().parse(request)
        serializer = PacketSerializer(data=data)
        if serialzier.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.error, status=400)
    return JsonResponse({"Access Deneid" : "You have not permision to edit this packet"}, status=400)


@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@api_view(['POST'])
def upload_file(request):
    data = request.data # is needed ?
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
    offer = Offer.objects.filter(packet=packet)
    serializer = OfferSerializer(offer, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def offer(request):
    # user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        slug = request.data.get("packet")
        price = request.data.get("price")
        description = request.data.get("description")
        travel_slug = request.data.get("travel")
        packet = Packet.objects.get(slug=slug)
        print(packet)
        travel = Travel.objects.get(slug=travel_slug)
        print(travel)
        data = request.data
        print(data)
        serializer = OfferDeserializer(data=data)
        if serializer.is_valid():
            serializer.save(packet=packet, travel=travel)
            packet.offer_count_inc()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    if request.method == 'PUT':
        slug = request.data.get("slug")
        offer = Offer.objects.get(slug=slug)
        if request.data.get("type") == 'ACCEPT':
            offer.status = '1'
            offer.save()
            return HttpResponse(status=200)
        if request.data.get("type") == 'REJECT':
            offer.status = '2'
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
