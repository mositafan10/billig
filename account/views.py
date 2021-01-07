from django.http import JsonResponse
from django.db.models import Q
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

from core.utils import validate_phonenumber ,validate_socailaddress ,generate_otp, verify_otp, set_otp, send_sms, locate_ip, setPhoneCache
from core.constant import WelcomeText, WelcomeText1, WelcomeText2, WelcomeText3


@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request, pk):
    try:
        user = User.objects.get(slug=pk)
    except User.DoesNotExist:
        raise NotFound
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
    password = request.data.get('password','')
    if password != '':
        try:
            password_validation.validate_password(password)
        except:
            detail=_("رمز انتخاب شده معتبر نیست")
            raise ValidationError({"detail": detail})
    try:
        user = User.objects.get(phone_number=new_phone_number)
        detail=_(".این شماره قبلا در سایت ثبت‌نام شده است")
        return JsonResponse({"detail": detail},status=403)
    except:
        otp = generate_otp()
        print(otp)
        # Here is good in set_otp we check that a how many time the user is insert the phone number :
        if setPhoneCache(new_phone_number):
            set_otp(new_phone_number, otp)
            send_sms(new_phone_number, otp)
            return HttpResponse(status=200)
        else:
            detail=_("لطفا چند دقیقه صبر نمایید")
            raise PermissionDenied({"detail": detail})
    

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_complete(request): 
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    password = request.data.get('password')
    name = request.data.get('name', '')
    otp = request.data.get('otp', '')
    # For showing the welcome page in client side 
    first_time = False
    if otp != '':
        otps = str(otp)
        if verify_otp(new_phone_number, otps):
            user, is_created = User.objects.get_or_create(phone_number=new_phone_number)
            if is_created is True:
                token, is_created = Token.objects.get_or_create(user=user)
                profile, is_created = Profile.objects.get_or_create(user=user)
                user.set_password(password)
                user.name = name
                user.save()
                first_time = True

                # Check ip and detect country of user 
                ip = request.META['REMOTE_ADDR'] 
                try:
                    country_eng = locate_ip(ip)
                except:
                    country_eng = None
                try:
                    country = Country.objects.get(eng_name=country_eng) 
                except:
                    country = None
                profile.country = country
                profile.save()

                # Create a chat conversation between admin and the user and send user welcome text
                admin = User.objects.get(pk=1)
                conversation, is_created = Conversation.objects.get_or_create(sender=admin, receiver=user)
                Massage.objects.create(chat_id=conversation, text='{} {}'.format(WelcomeText,user.name), owner=admin)
                Massage.objects.create(chat_id=conversation, text=(WelcomeText1), owner=admin)
                Massage.objects.create(chat_id=conversation, text=(WelcomeText2), owner=admin)
                Massage.objects.create(chat_id=conversation, text=(WelcomeText3), owner=admin)
                return JsonResponse({"token": str(token.key), "user": user.slug, "first_time": first_time})
            else:
                detail=_(".این شماره همراه قبلا در سایت ثبت‌نام شده است")
                raise AuthenticationFailed({"detail":detail})
        else:
            if setPhoneCache(new_phone_number):
                detail = _("کد وارد شده اشتباه است .مجدد سعی کنید ")
                raise AuthenticationFailed({"detail":detail})
            else:
                detail=_("لطفا چند دقیقه صبر نمایید")
                raise PermissionDenied({"detail": detail})
    else:
        detail=_("کد وارد نشده است")
        raise ValidationError({"detail":detail})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    password = request.data.get('password')
    first_time = False
    try:
        user = User.objects.get(phone_number=new_phone_number)
        # Check the user is active or not 
        if user.is_active:
            if not user.check_password(password):
                raise AuthenticationFailed(detail=_(".رمز عبور اشتباه است. مجدد تلاش کنید"))
            token = Token.objects.get(user=user)
            return JsonResponse({"token": str(token.key), "user": user.slug, "first_time": first_time})
        else:
            raise AuthenticationFailed(detail=_(".حساب کاربری شما غیرفعال شده است."))
    except User.DoesNotExist:
        raise AuthenticationFailed(detail=_(".نام کاربری در سایت یافت نشد. ابتدا در سایت ثبت نام کنید"))        


@permission_classes([AllowAny])
@api_view(['POST'])
def reset_password(request):
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    try:
        user = User.objects.get(phone_number=new_phone_number)
    except User.DoesNotExist:
        raise AuthenticationFailed(detail=_("شماره در سایت یافت نشد"))
    otp = generate_otp()
    if setPhoneCache(new_phone_number):
        set_otp(new_phone_number, otp)
        # Maybe here need to use try/except when api of sms dose not work TODO
        send_sms(phone_number, otp)
        return HttpResponse(status=200)
    else:
        detail=_("لطفا چند دقیقه صبر نمایید")
        raise PermissionDenied({"detail": detail})


@permission_classes([AllowAny])
@api_view(['POST'])
def confirm_reset_password(request):
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    otp = request.data.get('otp')
    otps = str(otp)
    if verify_otp(new_phone_number, otps):
        return JsonResponse({"detail":True})
    else:
        raise ValidationError(detail=_("کد وارد شده اشتباه است"))

@permission_classes([AllowAny])
@api_view(['POST'])
def new_password(request):
    phone_number = request.data.get('phone_number')
    new_phone_number = validate_phonenumber(phone_number)
    user = User.objects.get(phone_number=new_phone_number)
    password = request.data.get('new_password')
    try:
        password_validation.validate_password(password)
    except:
        raise ValidationError(detail=_("رمز عبور باید شامل یک حرف باشد"))
    user.set_password(password)
    user.save()
    return JsonResponse({"detail":_("رمز عبور با موفقیت تغییر پیدا کرد.")},status=200)


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
    countries = Country.objects.all().exclude(is_active=False).order_by('updated_at')
    serializer = CountrySerializer(countries, many=True)
    return JsonResponse(serializer.data, safe=False)

 
@permission_classes([permissions.AllowAny])
@api_view(['GET'])
def city_list(request, pk):
    cities = City.objects.filter(country=pk).order_by('updated_at')
    serializer = CitySerializer(cities, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)
    serializer = LimitedProfileSerializer(profile)

    # calculate total not_seen massage for user
    conversations = Conversation.objects.filter(Q(sender=user) | Q(receiver=user))
    total = 0
    for conversation in conversations:
        total += conversation.not_seen 
    return JsonResponse({"data":serializer.data ,"total":total})


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
        except:
            detail1={"detail" :_("رمز عبور باید شامل یک حرف باشد")}
            raise ValidationError(detail1)
        if current_password == new_password:
            print("hi")
            detail={"detail" :_(".رمز عبور جدید مشابه قبلی است")}
            raise ValidationError(detail)
        else:
            user.set_password(new_password)
            user.save()
            return HttpResponse(status=200)

        
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user) 
    comment = Score.objects.filter(reciever=profile)
    serializer = ScoreSerializer(comment, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myComment(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user) 
    comment = Score.objects.filter(owner=profile)
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
        # Check the @ before address
        address = request.data.get('address')
        new_address = validate_socailaddress(address)
        data = {
            "account_type": request.data.get('account_type'),
            "address": new_address
        }

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
        if token.user.is_active:
            return JsonResponse({"valid":True})
        else:
            detail = _("حساب کاربری شما غیر فعال شده است")
            raise PermissionDenied(detail=detail)
    except Token.DoesNotExist:
        return JsonResponse({"valid":False})

    