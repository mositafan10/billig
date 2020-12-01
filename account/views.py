from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, password_validation
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

from .models import Profile, Score, City, Country, User, Social
from .serializers import *
from .permissions import IsOwnerProfileOrReadOnly
from advertise.models import Offer 
from chat.models import Conversation, Massage
from datetime import datetime

from core.utils import validate_phonenumber, generate_otp, verify_otp, set_otp, send_sms, locate_ip
from core.constant import WelcomeText


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


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request): 
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    password = request.data.get('password')
    try:
        password_validation.validate_password(password)
    except:
        raise ValidationError(detail=_("رمز عبور باید شامل یک حرف باشد"))
    try:
        user = User.objects.get(phone_number=new_phone_number)
        raise AuthenticationFailed(detail=_(".این شماره قبلا در سایت ثبت‌نام شده است"))
    except:
        otp = generate_otp()
        set_otp(new_phone_number, otp)
        send_sms(new_phone_number, otp)
        return HttpResponse(status=200)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_complete(request): 
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    # Check ip and detect country of user 
    ip = request.META['REMOTE_ADDR'] 
    country_eng = locate_ip(ip)
    try:
        country = Country.objects.get(eng_name=country_eng) 
    except:
        country = None
    password = request.data.get('password')
    name = request.data.get('name', '')
    otp = request.data.get('otp', '')
    # For showing the welcome page in client side 
    first_time = False
    if otp != '':
        otps = str(otp)
        if verify_otp(new_phone_number, otps):
            user, is_created = User.objects.get_or_create(phone_number=new_phone_number)
            profile = Profile.objects.create(user=user)
            # Create a chat conversation between admin and the user and send user welcome text
            admin = User.objects.get(pk=1)
            conversation = Conversation.objects.create(sender=admin, receiver=user)
            massage = Massage.objects.create(chat_id=conversation, text=_(WelcomeText), owner=admin)
            if is_created is True:
                user.set_password(password)
                user.name = name
                user.save()
                profile.country = country
                profile.save()
                first_time = True
                token = Token.objects.create(user=user)
                # Is this needed to send refresh in response ( I think not and that was for jwt ) TODO
                return JsonResponse({"token": str(token.key),"refresh": str(token.key), "user": user.slug, "first_time": first_time})
            else:
                raise AuthenticationFailed(detail=_(".این شماره همراه قبلا در سایت ثبت‌نام شده است"))
        else:
            error = _("کد وارد شده اشتباه است .مجدد سعی کنید ")
            raise AuthenticationFailed(detail=error)
    else:
        raise ValidationError(detail=_("کد وارد نشده است"))


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    password = request.data.get('password')
    first_time = False
    try:
        user = User.objects.get(phone_number=phone_number)
        if not user.check_password(password):
            raise AuthenticationFailed(detail=".رمز عبور اشتباه است. مجدد تلاش کنید")
        user.last_login = datetime.now()
        user.save()
        token = Token.objects.get(user=user)
        # Is this needed to send refresh in response ( I think not and that was for jwt ) TODO
        return JsonResponse({"token": str(token.key),
            "refresh": str(token.key), "user": user.slug, "first_time": first_time})
    except User.DoesNotExist:
        raise AuthenticationFailed(detail=_(".نام کاربری در سایت یافت نشد. ابتدا در سایت ثبت نام کنید"))        


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
        raise AuthenticationFailed(detail=_("شماره در سایت یافت نشد"))


@permission_classes([AllowAny])
@api_view(['POST'])
def confirm_reset_password(request):
    phone_number = request.data.get('phone_number')
    user = User.objects.get(phone_number=phone_number)
    otp = request.data.get('otp')
    otps = str(otp)
    if verify_otp(phone_number, otps):
        user.set_password(otps)
        user.save()
        return JsonResponse({"detail":_("رمز عبور به کد ارسال شده تغییر پیدا کرد.")},status=200)
    else:
        raise AuthenticationFailed(detail="کد وارد شده اشتباه است")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    data = request.data
    serializer = ProfileDeserializer(data=data)
    if serializer.is_valid():
        try:
            country = Country.objects.get(pk=request.data.get("country")) 
            profile.country = country
        except:
            country = None
        try:
            name = request.data.get("name")
            user.name = name
        except:
            country = None
        try:
            city = City.objects.get(pk=request.data.get("city"))
            profile.city = city
        except:
            city = None
        try:
            email = request.data.get("email")
            profile.email = email
        except:
            email = None
        try:    
            account_owner = request.data.get("account_owner")
        except:
            account_owner = None
            profile.account_owner = account_owner
        try:
            account_number = request.data.get("account_number")
            profile.account_number = account_number
        except :
            account_number = None
        profile.save()
        user.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)


@permission_classes([permissions.AllowAny])
@api_view(['GET'])
def country_list(request):
    countries = Country.objects.all().exclude(is_active=False)
    serializer = CountrySerializer(countries, many=True)
    return JsonResponse(serializer.data, safe=False)

 
@permission_classes([permissions.AllowAny])
@api_view(['GET'])
def city_list(request, pk):
    cities = City.objects.filter(country=pk)
    serializer = CitySerializer(cities, many=True)
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
 

# Is this useable  TODO
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
        raise AuthenticationFailed(detail=_(".رمز عبور فعلی اشتباه است"))
    else:
        new_password = request.data.get('new_password')
        try:
            password_validation.validate_password(new_password)
            if current_password == new_password:
                raise ValidationError(detail=_(".رمز عبور جدید مشابه قبلی است"))
            else:
                user.set_password(new_password)
                user.save()
                return HttpResponse(status=200)
        except:
            raise ValidationError(detail=_("رمز عبور باید شامل یک حرف باشد"))

        
# There is extra query by profile. why ? TODO
# Slug should send by url not by body TODO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rating(request):
    owner_user = User.objects.get(pk=request.user.id)
    owner = Profile.objects.get(user=owner_user)
    receiver_user = User.objects.get(slug=request.data.get('receiver'))
    receiver = Profile.objects.get(user=receiver_user)
    slug = request.data.get('slug')
    offer = Offer.objects.get(slug=slug)
    score = request.data.get('score')
    text = request.data.get('comment')
    serializer = ScoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=owner, reciever=receiver)
        offer.status = '7'
        offer.save()
        return HttpResponse(status=200)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def rate_user_list(request, user):
    user = User.objects.get(slug=user)
    profile = Profile.objects.get(user=user)
    scores = Score.objects.filter(reciever=profile)
    serializer = ScoreSerializer(scores, many=True)
    return JsonResponse(serializer.data, safe=False)

# These are same TODO

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user) 
    comment = Score.objects.filter(reciever=profile)
    serializer = ScoreSerializer(comment, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST','GET'])
@permission_classes([AllowAny])
def comments_billlig(request):
    if request.method == 'GET':
        comments = CommentUser.objects.filter(is_approved=True)[:5]
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        try:
            user = Token.objects.get(pk=request.data.get('token')).user
            profile = Profile.objects.get(user=user)
        except:
            user = None
            profile = None
        data = request.data
        serializer = CommentDeserializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=profile)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


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
        raise APIException(detail=_("ایمیل شما قبلا ثبت شده است"))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def social(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    try:
        social = Social.objects.get(profile=profile, account_type=request.data.get("account_type"))
        raise PermissionDenied(detail=_("این اکانت قبلاً ایجاد شده است"))
    except Social.DoesNotExist:
        data= request.data
        serializer = SocialDeserializer(data=data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

        
@api_view(['GET'])
@permission_classes([AllowAny])
def social_pub(request, slug):
    user = User.objects.get(slug=slug)
    profile = Profile.objects.get(user=user)
    social_list = Social.objects.filter(profile=profile)
    serializer = SocialSerializer(social_list, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def social_delete(request, slug):
    social = Social.objects.get(slug=slug)
    social.delete()
    return HttpResponse(status=204)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_validation(request):
    token = request.data.get('token')
    try:
        token = Token.objects.get(key=token)
        return JsonResponse({"valid":True})
    except Token.DoesNotExist:
        return JsonResponse({"valid":False})

    