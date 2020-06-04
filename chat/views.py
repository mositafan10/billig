import json

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework import status, permissions
# from rest_framework.parsers import JSONParse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view, permission_classes, parser_classes

from .serializers import MassageSerializer
from .models import Massage


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def chat_list(request):
    if request.method == 'GET':
        massage = Massage.objects.all()
        serializer = MassageSerializer(massage, many=True,)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        print(request)
        #data = MultiPartParser().parse(request.data)
        data = request.data
        print(data)
        serializer = MassageSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)