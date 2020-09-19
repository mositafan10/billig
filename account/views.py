from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, permissions, generics
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.exceptions import PermissionDenied, ValidationError, AuthenticationFailed, APIException, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

from .utils import generate_otp, set_otp, verify_otp, send_sms
from .models import Profile, Score, City, Country, User
from .serializers import *
from .permissions import IsOwnerProfileOrReadOnly
from advertise.models import Offer 

from datetime import datetime


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile)
    return JsonResponse(serializer.data, safe=False)


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerProfileOrReadOnly]


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def signup(request): 
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    name = request.data.get('name')
    otp = generate_otp()
    set_otp(phone_number, otp)
    print(otp)
    # send_sms(phone_number, otp)
    return HttpResponse(status=200)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([permissions.AllowAny])
def login(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    name = request.data.get('name', '')
    refresh = None
    first_time = False

    # for first login
    otp = request.data.get('otp', '')
    if otp != '':
        if verify_otp(phone_number, otp):
            user, is_created = User.objects.get_or_create(phone_number=phone_number)
            profile, is_created = Profile.objects.get_or_create(user=user)
            if is_created is True:
                user.set_password(password)
                user.name = name
                user.save()
                first_time = True
        else :
            error = "کد وارد شده اشتباه است .مجدد سعی کنید "
            raise AuthenticationFailed(detail=error)

    # Not first time
    try:
        user = User.objects.get(phone_number=phone_number)
        if not user.check_password(password):
            raise AuthenticationFailed(detail=".رمز عبور اشتباه است. مجدد تلاش کنید")
        user.last_login = datetime.now()
        user.save()
        refresh = RefreshToken.for_user(user)
        return JsonResponse({"token": str(refresh.access_token),
            "refresh": str(refresh), "user": user.id, "first_time": first_time})
    except User.DoesNotExist:
        raise AuthenticationFailed(detail=".نام کاربری در سایت یافت نشد. ابتدا در سایت ثبت نام کنید")        


@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@api_view(['POST'])
def reset_password(request):
    phone_number = request.data['phone_number']
    try:
        user = User.objects.get(phone_number=phone_number)
        otp = generate_otp()
        set_otp(phone_number, otp)
        print(otp)
        # send_sms(phone_number, otp)
        return HttpResponse(status=200)
    except User.DoesNotExist:
        raise AuthenticationFailed(detail="User not found !")


@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@api_view(['POST'])
def confirm_reset_password(request):
    phone_number = request.data['phone_number']
    otp = request.data['otp']
    user = User.objects.get(phone_number=phone_number)
    if verify_otp(phone_number, otp):
        user.set_password(otp)
        user.save()
        return HttpResponse(status=200)
    else:
        raise AuthenticationFailed(detail="عدد وارد شده اشتباه است")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_user(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    country = Country.objects.get(pk=request.data.get("country"))   
    city = City.objects.get(pk=request.data.get("city"))
    data = request.data
    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
        profile.bio = request.data.get("bio")
        profile.facebook_id = request.data.get("facebook_id")
        profile.instagram_id = request.data.get("instagram_id")
        profile.twitter_id = request.data.get("twitter_id")
        profile.linkdin = request.data.get("bio")
        profile.email = request.data.get("email")
        profile.country = country
        profile.city = city
        profile.save()
        user.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)


@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([permissions.AllowAny])
@api_view(['GET','POST'])
def country_list(request):
    if request.method == 'GET':
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        serializer = CountrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
 


@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([permissions.AllowAny])
@api_view(['GET','POST'])
def city_list(request, pk):
    if request.method == 'GET':
        cities = City.objects.filter(country=pk)
        serializer = CitySerializer(cities, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        serializer = CitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def friend_request(request):
    request_by = User.objects.get(pk=request.user.id)
    data = request.data
    serializer = FollowSerializer(data=data)
    if serializer.is_valid():
        serializer.save(follower = request_by)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_list(request):
    user = User.objects.get(pk=request.user.id)
    friend = Follow.objects.filter(follower = user)
    serializer = FollowSerializer(friend, many=True)
    return JsonResponse(serializer.data, safe=False)


#for authentication test
class CheckAuth(generics.GenericAPIView):

    def post(self, request):
        print(request.user)
        print(request.user.id)
        if request.user.is_authenticated:
             content = {'message': 'Authenticated'}
             return Response(content, status=200)
        else:
             content = {'message': 'Unauthenticated'}
             return Response(content, status=401)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request):
    user = User.objects.get(pk=request.user.id)
    print(user)
    profile = Profile.objects.get(user=user)
    print(profile)
    return JsonResponse({"user":profile.user.name})


@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@api_view(['POST'])
def upload_file(request):
    user = User.objects.get(pk=request.user.id)
    data = request.data # is needed ?
    profile = Profile.objects.get(user=user) 
    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
        profile.picture = request.FILES.get('avatar')
        profile.save()
        return JsonResponse(str(profile.picture), safe=False)
    return JsonResponse(serializer.errors, status=400)
 

@permission_classes([IsAuthenticated]) 
@api_view(['GET'])
def logout(request):
    user = User.objects.get(pk=request.user.id)
    user.last_logout = datetime.now()
    user.save()
    return HttpResponse(status=200)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def change_password(request):
    user = User.objects.get(pk=request.user.id)
    current_password = request.data.get('current_password')
    if not user.check_password(current_password):
        raise AuthenticationFailed(detail=".رمز عبور فعلی اشتباه است. مجدد تلاش کنید")
    else:
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return HttpResponse(status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rating(request):
    owner_user = User.objects.get(pk=request.user.id)
    owner = Profile.objects.get(user=owner_user)
    receiver_user = User.objects.get(pk=request.data.get('receiver'))
    receiver = Profile.objects.get(user=receiver_user)
    slug = request.data.get('slug')
    offer = Offer.objects.get(slug=slug)
    score = request.data.get('score')
    text = request.data.get('comment')
    receiver = Profile.objects.get(user=receiver_user)
    serializer = ScoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=owner, reciever=receiver)
        offer.status = '7'
        offer.save()
        return HttpResponse(status=200)
    return JsonResponse(serializer.errors, status=400)



@api_view(['POST'])
@permission_classes([AllowAny])
def newsletter(request):
    if not Newsletter.objects.filter(email=request.data.get('email')).exists():
        data = request.data
        serializer = NewsletterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializers.errors, status=400)
    else:
        raise APIException(detail="ایمیل شما قبلا ثبت شده است")