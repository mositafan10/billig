from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

from rest_framework import status, permissions, generics
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.exceptions import PermissionDenied, ValidationError, AuthenticationFailed, APIException, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from .utils import OTP ,send_sms, validate_phonenumber
from .models import Profile, Score, City, Country, User, Social
from .serializers import *
from .permissions import IsOwnerProfileOrReadOnly
from advertise.models import Offer 

from datetime import datetime


@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request, pk):
    user = User.objects.get(slug=pk)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_private(request, pk):
    user = User.objects.get(slug=pk)
    profile = Profile.objects.get(user=user)
    serializer = PrivateProfileSerializer(profile)
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
    new_phone_number = validate_phonenumber(phone_number)
    user = User.objects.filter(phone_number=new_phone_number).count()
    if user == 0:
        otp = OTP.generate_otp()
        OTP.set_otp(new_phone_number, otp)
        send_sms(phone_number, otp)
        return HttpResponse(status=200)
    else:
        raise AuthenticationFailed(detail=_(".این شماره همراه قبلا در سایت ثبت‌نام شده است"))


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def signup_complete(request): 
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    password = request.data.get('password')
    name = request.data.get('name', '')
    first_time = False
    refresh = None
    otp = request.data.get('otp', '')
    if otp != '':
        otps = str(otp)
        if OTP.verify_otp(new_phone_number, otps):
            user, is_created = User.objects.get_or_create(phone_number=new_phone_number)
            profile, is_created = Profile.objects.get_or_create(user=user)
            if is_created is True:
                user.set_password(password)
                user.name = name
                user.save()
                first_time = True
                token = Token.objects.create(user=user)
                return JsonResponse({"token": str(token.key),"refresh": str(token.key), "user": user.slug, "first_time": first_time})
            else:
                raise AuthenticationFailed(detail=_(".این شماره همراه قبلا در سایت ثبت‌نام شده است"))
        else:
            error = _("کد وارد شده اشتباه است .مجدد سعی کنید ")
            raise AuthenticationFailed(detail=error)
    else:
        raise ValidationError(detail=_("کد وارد نشده است"))


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([permissions.AllowAny])
def login(request):
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    password = request.data.get('password')
    refresh = None
    first_time = False
    try:
        user = User.objects.get(phone_number=phone_number)
        if not user.check_password(password):
            raise AuthenticationFailed(detail=".رمز عبور اشتباه است. مجدد تلاش کنید")
        user.last_login = datetime.now()
        user.save()
        token = Token.objects.get(user=user)
        return JsonResponse({"token": str(token.key),
            "refresh": str(token.key), "user": user.slug, "first_time": first_time})
    except User.DoesNotExist:
        raise AuthenticationFailed(detail=".نام کاربری در سایت یافت نشد. ابتدا در سایت ثبت نام کنید")        


@permission_classes([AllowAny])
@api_view(['POST'])
def reset_password(request):
    phone_number = request.data.get('phone_number')
    try:
        user = User.objects.get(phone_number=phone_number)
        otp = generate_otp()
        set_otp(phone_number, otp)
        send_sms(phone_number, otp)
        return HttpResponse(status=200)
    except User.DoesNotExist:
        raise AuthenticationFailed(detail="این شماره موبایل در سایت موجود نیست")


@permission_classes([AllowAny])
@api_view(['POST'])
def confirm_reset_password(request):
    phone_number = request.data.get('phone_number')
    otp = request.data.get('otp')
    user = User.objects.get(phone_number=phone_number)
    if verify_otp(phone_number, otp):
        user.set_password(otp)
        user.save()
        return JsonResponse({"detail":"رمز عبور به کد ارسال شده به شما تغییر پیدا کرد."},status=200)
    else:
        raise AuthenticationFailed(detail="عدد وارد شده اشتباه است")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_user(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    try:
        country = Country.objects.get(pk=request.data.get("country"))   
        city = City.objects.get(pk=request.data.get("city"))
    except:
        pass
    data = request.data
    serializer = ProfileDeserializer(data=data)
    if serializer.is_valid():
        try:
            profile.email = request.data.get("email")
        except:
            pass
        try:    
            profile.account_number = request.data.get("account_number")
            profile.account_owner = request.data.get("account_owner")
        except:
            pass
        try:
            profile.country = country
            profile.city = city
        except:
            pass
        profile.save()
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    serializer = LimitedProfileSerializer(profile)
    return JsonResponse(serializer.data)


@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@api_view(['POST'])
def upload_file(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user) 
    profile.picture = request.FILES.get('billlig')
    profile.save()
    return JsonResponse(str(profile.picture), safe=False)
 

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


@api_view(['GET'])
@permission_classes([AllowAny])
def comment(request, pk):
    user = User.objects.get(slug=pk)
    profile = Profile.objects.get(user=user) 
    comment = Score.objects.filter(reciever=profile)
    serializer = ScoreSerializer(comment, many=True)
    return JsonResponse(serializer.data, safe=False)


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def social(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    try:
        social = Social.objects.get(profile=profile, account_type=request.data.get("account_type"))
        raise PermissionDenied(detail=_("این اکانت از قبل ایجاد شده است"))
    except Social.DoesNotExist:
        data= request.data
        serializer = SocialDeserializer(data=data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

        
@api_view(['GET'])
@permission_classes([AllowAny])
def social_pub(request, pk):
    user = User.objects.get(slug=pk)
    profile = Profile.objects.get(user=user)
    social_list = Social.objects.filter(profile=profile)
    serializer = SocialSerializer(social_list, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def social_delete(request, pk):
    social = Social.objects.get(pk=pk)
    social.delete()
    return HttpResponse(status=204)
