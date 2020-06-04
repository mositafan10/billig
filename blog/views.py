from django.shortcuts import HttpResponse
from django.http import JsonResponse 
from .models import Post
from .serializers import PostSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from rest_framework.exceptions import ValidationError


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([AllowAny])
def post_detail(request, pk):
    try:
        posts = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = PostSerializer(posts)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        posts.delete()
        return HttpResponse(status=204)
    # else ?


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def like_post(request, pk):
    try:
        posts = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    ip = request.META.get("HTTP_REMOTE_ADDR")
    model_name = "like"
    key = '%s_%s' % (model_name, ip)
    if not cache.get(key) == pk:
        cache.set(key, pk, 2)
        Post.objects.get(pk=pk).like()
        return HttpResponse(status=201)
    return HttpResponse(status=400)

@api_view(['GET','POST'])
@permission_classes([AllowAny])    
def dislike_post(request, pk):
    try:
        posts = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    ip = request.META.get("HTTP_REMOTE_ADDR")
    model_name = "dislike"
    key = '%s_%s' % (model_name, ip)
    if not cache.get(key) == pk:
        cache.set(key, pk, 2)
        Post.objects.get(pk=pk).dislike()
        return HttpResponse(status=201)
    return HttpResponse(status=400)

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def visit_count(request, pk):
    try:
        posts = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    ip = request.META.get("HTTP_REMOTE_ADDR")
    model_name = "view"
    key = '%s_%s' % (model_name, ip)
    if not cache.get(key) == pk:
        cache.set(key, pk, 2)
        Post.objects.get(pk=pk).view()
        return HttpResponse(status=201)
    return HttpResponse(status=400)

@api_view(['GET','PUT','DELETE'])
@permission_classes([AllowAny])
def score(request, pk): 
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    ip = request.META.get("HTTP_REMOTE_ADDR")
    model_name = "score"
    value = int(request.GET['value'])
    key = '%s_%s' % (model_name, ip)
    if not cache.get(key) == pk:
        cache.set(key, pk, 2)
        post.calculate_score(value)
        return HttpResponse(status=201)
    return HttpResponse(status=400)
