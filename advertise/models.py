from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
from django.db import models

from rest_framework.exceptions import PermissionDenied, ValidationError

from account.models import User, BaseModel, Country, City, Profile
from core.utils import generate_slug
from core.constant import *

import string


class Packet(BaseModel):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    origin_country = models.ForeignKey(Country, on_delete = models.PROTECT, related_name="origin_country")
    origin_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="origin_city")
    destination_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="destination_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="destination_city")
    category = models.IntegerField(choices=PACKET_CATEGORY)
    category_other = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(validators=[MaxValueValidator(30.0),MinValueValidator(0.0)], max_digits=3, decimal_places=1)
    dimension = models.IntegerField(choices=DIMENSION)
    suggested_price = models.PositiveIntegerField(default=0)
    buy = models.BooleanField(default=False)
    phonenumber_visible = models.BooleanField(default=False)
    picture = models.IntegerField(default=1)
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    status = models.IntegerField(choices=PACKET_STATUS, default=10)
 
    def __str__(self):
        return str(self.id)

    def visit(self):
        self.visit_count += 1
        self.save()
    
    @property
    def owner_name(self):
        return str(self.owner.name)

    @property
    def owner_slug(self):
        return str(self.owner.slug)

    @property
    def parcel_price(self):
        return self.packet_info.get().price   
         
    @property
    def parcel_link(self):
        return self.packet_info.get().link   

    @property
    def phonenumber(self):
        return self.owner.phone_number

    def create(self):
        self.save()
        super().save(*args, **kwargs)
        return self.id 
    
    def save(self, *args, **kwargs):

        #chack same country
        if self.origin_country == self.destination_country:
            if self.origin_city == self.destination_city:
                raise PermissionDenied(detail="امکان یکی بودن مبدا و مقصد وجود ندارد")
        else:
            super().save(*args, **kwargs)

        
class Travel(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    departure = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="depar_country")
    departure_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="depar_city")
    destination = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="dest_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="dest_city")
    flight_date_start = models.DateField()
    flight_date_end = models.DateField(blank=True, null=True)
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    income = models.PositiveIntegerField(default=0)
    approved_packet = models.PositiveIntegerField(default=0)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True)
    status = models.IntegerField(choices=TRAVEL_STATUS, default=0)
    
    def __str__(self):
        return str(self.id)

    def visit(self):
        self.visit_count += 1
        self.save()

    def save(self, *args, **kwargs):
        if self.departure == self.destination:
            if self.departure_city == self.destination_city:
                raise PermissionDenied(detail="امکان یکی بودن مبدا و مقصد وجود ندارد")
            else:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
    

class Offer(BaseModel):
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, related_name="packet_ads")
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name="travel_ads")
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    slug = models.CharField(default=generate_slug, max_length=8, unique=True, editable=False)
    status = models.IntegerField(choices=Offer, default=0)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        #increase offer count of the packet
        if self.packet.status == 1:
            if self.status == 0:
                self.packet.offer_count += 1

            #update packet state due to offer state
            if (self.status > 1 and self.status != 8): 
                self.packet.status = self.status
            self.packet.save()
            super().save(*args, **kwargs)

        #first offer for packet
        elif self.packet.status == 0 :
            self.packet.status = 1
            self.packet.offer_count += 1
            self.packet.save()
            super().save(*args, **kwargs)

        elif (self.packet.status > 1):
            if self.status == 0:
                raise PermissionDenied(detail="این آگهی امکان دریافت پیشنهاد ندارد")
            elif (self.status != 1 and self.status != 8): 
                self.packet.status = self.status
                self.packet.save()
                super().save(*args, **kwargs)
            else:
                return None
        
        if self.status == 3 :
            self.travel.approved_packet += 1
            self.travel.income += self.price
            self.travel.save()
            super().save(*args, **kwargs)

    @property
    def receiver(self):
        return str(self.packet.owner.name)
    
    @property
    def sender(self):
        return str(self.travel.owner.name)

    @property
    def sender_id(self):
        return self.travel.owner.id
    
    @property
    def receiver_id(self):
        return self.packet.owner.id
    
    @property
    def sender_avatar(self):
        profile = Profile.objects.get(user=self.travel.owner)
        return str(profile.picture)

    @property
    def receiver_avatar(self):
        profile = Profile.objects.get(user=self.packet.owner)
        return str(profile.picture)

    @property
    def packet_slug(self):
        return self.packet.slug

    @property
    def packet_title(self):
        return self.packet.title

    @property
    def parcel_price(self):
        return self.packet.packet_info.get().price
    

class Bookmark(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bookmark_owner")
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, related_name="bookmark_packet")

    def __str__(self):
        return str(self.id)

    @property
    def packet_title(self):
        return str(self.packet.title)
    
    @property
    def packet_slug(self):
        return self.packet.slug


class Report(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reporter")
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE)
    title = models.CharField(max_length=15)
    text = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s --> %s" %(self.owner,self.packet)


class PacketPicture(BaseModel):
    image_file = models.FileField(upload_to='images/%Y/%m',)
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        MAX_FILE_SIZE = 10485760
        filesize = self.image_file.size
        if filesize > MAX_FILE_SIZE:
            raise ValidationError(detail=_("حجم تصویر بیش از حد زیاد است"))
        else:
            super().save(*args, **kwargs)


class Buyinfo(BaseModel):
    packet = models.ForeignKey('Packet', on_delete=models.CASCADE, related_name="packet_info")
    link = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)