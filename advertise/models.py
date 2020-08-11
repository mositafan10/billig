import string

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.db import IntegrityError
from django.db import models

from account.models import User, BaseModel, Country, City, Profile
from .utils import generate_slug

PACKET_STATUS = [
        (0, "در انتظار تایید"),
        (1, "عدم تایید"),
        (2, "منتشر شده"),
        (3, "دارای پیشنهاد"),
        (4, "منقضی شده"),
        (5, "حذف شده"),
        (6, "در انتظار پرداخت"),
        (7, "در انتظار خرید"),
        (8, "خریداری شده"),
        (9, "در حال ارسال"),
        (10, "انجام شده"),
] 

TRAVEL_STATUS = [
        (0, "در انتظار تایید"),
        (1, "عدم تایید"),
        (2, "منتشر شده"),
        (3, "دارای بسته"),
        (4, "انجام شده"),
        (5, "حذف شده"),
] 

Offer = [
        (0, "در انتظار پاسخ"),
        (1, "تایید"),
        (2, "عدم تایید"),
        (3, "در انتظار پرداخت"),
        (4, "در انتظار خرید"),
        (5, "خریداری شده"),
        (6, "در حال ارسال"),
        (7, "انجام شده"),
        (8, "در حال مذاکره")
] 

# for other choice we need a field to be filled by user about category TODO
PACKET_CATEGORY = [
        (0, "مدارک و مستندات"),
        (1, "کتاب و مجله"),
        (2, "لوازم الکترونیکی"),
        (3, "کفش و پوشاک"),
        (4, "لوازم آرایشی و بهداشتی"),
        (5, "سایر موارد"),
]
    

class Packet(BaseModel):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    origin_country = models.ForeignKey(Country, on_delete = models.PROTECT, related_name="origin_country")
    origin_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="origin_city")
    destination_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="destination_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="destination_city")
    category = models.IntegerField(choices=PACKET_CATEGORY)
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(30),MinValueValidator(1)])
    suggested_price = models.PositiveIntegerField()
    buy = models.BooleanField(default=False)
    picture = models.ManyToManyField('PacketPicture', blank=True, related_name="packets")
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    # should not be send by user: this should be validate
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    status = models.IntegerField(choices=PACKET_STATUS, default=0)
 
    def __str__(self):
        return str(self.id)

    def visit(self):
        self.visit_count += 1
        self.save()
    
    def offer_count_inc(self):
        self.offer_count += 1
        if self.status == '2':
            self.status == '3'
        self.save()
    
    @property
    def owner_firstname(self):
        return str(self.owner.first_name + ' ' + self.last_name)
    

class Travel(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    departure = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="depar_country")
    departure_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="depar_city")
    destination = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="dest_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="dest_city")
    empty_weight = models.PositiveIntegerField(validators=[MaxValueValidator(30),MinValueValidator(1)], blank=True, null=True) 
    flight_date_start = models.DateField()
    flight_date_end = models.DateField(blank=True, null=True)
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
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
    description = models.TextField()
    slug = models.CharField(default=generate_slug, max_length=8, unique=True, editable=False)
    status = models.IntegerField(choices=Offer, default=0)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.packet.status = '3' 
        self.packet.save()
        super().save(*args, **kwargs)
    
    def packet_offer_count(self):
        self.packet.offer_count += 1
        self.packet.save()
        super().save(*args, **kwargs)

    @property
    def receiver(self):
        return str(self.packet.owner.first_name + ' ' + self.packet.owner.last_name)
    
    @property
    def sender(self):
        return str(self.travel.owner.first_name + ' ' + self.travel.owner.last_name)

    @property
    def sender_id(self):
        return self.travel.owner.id

    @property
    def packet_slug(self):
        return self.packet.slug
        
      
class Bookmark(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="bookmark_owner")
    advertise = models.ForeignKey(Packet, on_delete=models.PROTECT, blank=True, null=True)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Report(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reporter")
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
