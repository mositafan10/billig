import string

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.db import IntegrityError
from django.db import models

from rest_framework.exceptions import PermissionDenied

from account.models import User, BaseModel, Country, City, Profile
from .utils import generate_slug

TRAVEL_STATUS = [
        (0, "در انتظار تایید"),
        (1, "عدم تایید"),
        (2, "منتشر شده"),
        (3, "دارای بسته"),
        (4, "انجام شده"),
        (5, "حذف شده"),
        (6, "تسویه شده"),
] 

PACKET_STATUS = [
        (0, "منتشر شده"),
        (1, "دارای پیشنهاد"),
        (2, "در انتظار پرداخت"),
        (3, "در انتظار خرید"),
        (4, "در انتظار تحویل"),
        (5, "در انتظار تایید خریدار"),
        (6, "انجام شده"),
        (7, "تمام شده"),
        (8, "حذف شده"),
        (9, "منقضی شده"),
        (10, "در انتظار تایید"),
        (11, "عدم تایید"),
] 

Offer = [
        (0, "در انتظار پاسخ"), # default state
        (1, "در انتظار تایید مسافر"),# done by packet owner when accept offer : offer_update in advertise.view
        (2, "در انتظار پرداخت"), # done by traveler after confirm the price : offer_update in advertise.view
        (3, "در انتظار خرید"), # done after payment : verify function in payment.view
        (4, "در انتظار تحویل"),# done by traveler after buy parcel : offer_update function in advertise.view
        (5, "در انتظار تایید خریدار"), # done by traveler after get parcel in destination : offer_update function in advertise.view
        (6, "انجام شده"),# done by packet owner when receive parcel in destination : offer_update in advertise.view
        (7, "تمام شده"), # done after rating by packet owner in account.view
        (8, "حذف شده"), # done by offer owner : offer_update in advertise.view
] 

# for other choice we need a field to be filled by user about category TODO
PACKET_CATEGORY = [
        (0, "مدارک و مستندات"),
        (1, "کتاب و مجله"),
        (2, "لوازم الکترونیکی"),
        (3, "کفش و پوشاک"),
        (4, "لوازم آرایشی و بهداشتی"),
        (5, "دارو"),
        (6, "سایر موارد"),
]

DIMENSION = [
        (0, "حیلی کوچک"),
        (1, "کوچک"),
        (2, "متوسط"),
        (3, "بزرگ"),
        (4, "خیلی بزرگ"),
]
    

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
    suggested_price = models.PositiveIntegerField()
    buy = models.BooleanField(default=False)
    
    # foreignkey is ok !
    picture = models.IntegerField(blank=True, null=True)
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    # should not be send by user: this should be validate
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
            elif (self.status > 1 and self.status != 8): 
                self.packet.status = self.status
                self.packet.save()
                super().save(*args, **kwargs)
            else:
                return None

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
    def packet_slug(self):
        return self.packet.slug

    @property
    def packet_title(self):
        return self.packet.title
        
      
class Bookmark(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bookmark_owner")
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE)

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
    image_file = models.FileField(upload_to='images/%Y/%m')
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Buyinfo(BaseModel):
    packet = models.ForeignKey('Packet', on_delete=models.CASCADE, related_name="packet_info")
    link = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)