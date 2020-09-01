from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .utils import validate_picture
from django.contrib.auth.models import PermissionsMixin


# User = get_user_model()

Follow_Choices = [
    ('0','در انتظار'),
    ('1','تایید'),
    ('2','رد')
]

Level = [
    ('1', 'Gold'),
    ('2', 'Silver'),
    ('3', 'Bronz'),
]


class BaseModel (models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
       
        if not phone_number:
            raise ValueError("شماره موبایل خود را وارد کنید")
        
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        print(phone_number)
        if password is None :
            raise TypeError("ایمیل وارد کن")
        user = self.create_user(phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, editable=False)
    phone_number = models.CharField(max_length=15, editable=False, unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True, default="کاربر")
    last_name = models.CharField(max_length=20, blank=True, null=True, default="جدید")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    USERNAME_FIELD = 'phone_number'
    last_logout = models.DateTimeField(_('last logout'), blank=True, null=True)

    objects = UserManager()
    
    def __str__(self):  
        return "{}".format(self.phone_number)


class Profile (BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.ImageField(blank=True, null=True, upload_to='images/profile_picture/%Y/%m') #need default
    bio = models.TextField(blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, blank=True, null=True) # default = get from address or ip
    city = models.ForeignKey('City', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    favorite_gift = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=1, choices=Level, default='3')
    score = models.DecimalField(default=0.0, max_digits=3, decimal_places=1)
    scores_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=50, blank=True, null=True)
    instagram_id = models.CharField(max_length=50, blank=True, null=True)
    twitter_id = models.CharField(max_length=50, blank=True, null=True)
    linkdin_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def name(self):
        return str(self.user.first_name + ' ' + self.user.last_name )
    
# can be removed
class Social(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    social_id = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
        

class Score(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    reciever = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='score_receiver')
    score = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return "%s --> %s" % (self.owner, self.reciever)

    def save(self, *args, **kwargs):
        scores_count = self.reciever.scores_count
        self.reciever.score = (self.reciever.score * scores_count + self.score)/(scores_count + 1)
        self.reciever.scores_count += 1
        self.reciever.save()
        super().save(*args, **kwargs)


class CommentUser(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_give_comment")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_receive_comment")
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s --> %s" % (self.owner, self.receiver)
    
    def save(self, *args, **kwargs):
        check_duplicate = CommentUser.objects.filter(owner=self.owner, receiver=self.receiver)
        if not check_duplicate:
            self.owner.comment_count += 1
            self.owner.save()
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            raise ValidationError("It's done before. thank you again") #???? TODO


class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    status = models.CharField(max_length=10 ,choices=Follow_Choices, default=0)

    def __str__(self):
        return "%s --> %s" % (self.follower, self.following)

    def save(self, *args, **kwargs):
        # if self.follower != self.following:
        self.follower.following_count += 1
        self.follower.save()
        self.following.refresh_from_db()
        self.following.follower_count += 1
        self.following.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # if self.follower != self.following:
        self.follower.following_count -= 1
        self.follower.save()
        self.following.refresh_from_db()
        self.following.follower_count -= 1
        self.following.save()
        super().delete(*args, **kwargs)


class Country(BaseModel):
    name = models.CharField(max_length=15)
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


class PacketPicture(BaseModel):
    image_file = models.FileField(upload_to='images/Packet/%Y/%m')
