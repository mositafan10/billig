from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin

from core.utils import generate_slug
from core.constant import Social_Type, Level


class BaseModel (models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
       
        if not phone_number:
            raise ValueError(_("شماره موبایل خود را وارد کنید"))
        
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        if password is None :
            raise TypeError("ایمیل خود را وارد کنید")
        user = self.create_user(phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, editable=False)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=40, blank=True, null=True, default="کاربر جدید")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    USERNAME_FIELD = 'phone_number'

    objects = UserManager()
    
    def __str__(self):  
        return "{}".format(self.phone_number)


class Profile (BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(blank=True, null=True, upload_to='images/profile_picture/%Y/%m') 
    country = models.ForeignKey('Country', on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    level = models.CharField(max_length=1, choices=Level, default='3')
    score = models.DecimalField(default=0.0, max_digits=3, decimal_places=1)
    scores_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    travel_done = models.PositiveIntegerField(default=0)
    billlig_done = models.PositiveIntegerField(default=0)
    account_number = models.CharField(max_length=24, blank=True, null=True, validators=[RegexValidator(regex=r'^\d{1,24}$', message=_("شماره شبا نامعتبر است")), RegexValidator(regex='^.{24}$',message=_("شماره شبا می‌بایست ۲۴ رقم باشد"))])
    account_owner = models.CharField(max_length=50, blank=True, null=True)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    is_approved = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def name(self):
        return str(self.user.name)
    
    @property
    def phone_number(self):
        return str(self.user.phone_number)
    
    @property
    def joined_at(self):
        return str(self.create_at)
    
    
class Score(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    reciever = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='score_receiver')
    score = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    text = models.TextField()
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def owner_avatar(self):
        return str(self.owner.picture)

    @property
    def owner_name(self):
        return self.owner.user.name

    def save(self, *args, **kwargs):
        scores_count = self.reciever.scores_count
        self.reciever.score = (self.reciever.score * scores_count + self.score)/(scores_count + 1)
        self.reciever.scores_count += 1
        self.reciever.save()
        super().save(*args, **kwargs)


class Country(BaseModel):
    name = models.CharField(max_length=15)
    eng_name = models.CharField(max_length=15)
    icon = models.ImageField(blank=True, null=True, upload_to='images/country')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
  
    @property
    def city_list(self):
        return list(Country.objects.city.all())


class City(BaseModel):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="city")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Newsletter(BaseModel):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Social(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    account_type = models.CharField(max_length=20 ,choices=Social_Type)
    address = models.CharField(max_length=30)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 

    def __str__(self):
        return str(self.id)


class CommentUser(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def picture(self):
        return str(self.owner.picture)

    @property
    def name(self):
        return str(self.owner.user.name)

