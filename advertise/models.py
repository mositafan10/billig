from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
from django.db import models

from rest_framework.exceptions import PermissionDenied, ValidationError

from account.models import User, BaseModel, Country, City, Profile
from core.utils import generate_slug
from core.constant import TRAVEL_STATUS, PACKET_STATUS, Offer, DIMENSION
from chat.utils import send_to_chat
import string, json
from .utils import send_to_chat, send_admin_text, disable_chat, create_chat


class Packet(BaseModel):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    origin_country = models.ForeignKey(Country, on_delete = models.PROTECT, related_name="origin_country", null=True, blank=True)
    origin_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="origin_city", null=True, blank=True)
    no_matter_origin = models.BooleanField(default=False) 
    destination_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="destination_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="destination_city")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="category")
    category_other = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(validators=[MaxValueValidator(30.0),MinValueValidator(0.0)], max_digits=3, decimal_places=1)
    dimension = models.IntegerField(choices=DIMENSION)
    suggested_price = models.PositiveIntegerField(default=0)
    buy = models.BooleanField(default=False)
    phonenumber_visible = models.BooleanField(default=False) # should be removed TODO
    picture = models.CharField(default=1, max_length=8)
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=1000)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    status = models.IntegerField(choices=PACKET_STATUS, default=0)
 
    def __str__(self):
        return str(self.id)
    
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
    
    def save(self, *args, **kwargs):
        
        # Send admin text while create packet   
        if self._state.adding:
            send_admin_text(self.status, self.title, self.owner)

        #chack same country when packet is created
        if self.origin_country == self.destination_country:
            if self.origin_city == self.destination_city:
                raise PermissionDenied(detail=_("امکان یکی بودن مبدا و مقصد وجود ندارد"))
        
        # Send admin text
        if self.status == 10 or self.status == 11:
            send_admin_text(self.status, self.title, self.owner)
        
        # Increase number of billlig_done by user
        if self.status == 7:
            profile = Profile.objects.get(user=self.owner)
            profile.billlig_done += 1
            profile.save()
    
        # defualt picture
        if self.picture == 1:
            picture = PacketPicture.objects.get(pk=1)
            self.picture = picture.slug

        super().save(*args, **kwargs)
    
    # Question is if a owner of packet wnats to delete it, what do we do ? TODO
    # Check the correct error on frontend
    # when travel could be deleted then the all its offers should be deleted
    def delete(self, *args, **kwargs):
        if self.status == 3 or self.status == 4 or self.status == 5 or self.status == 6 :
            raise PermissionDenied(detail=_("با توجه به وضعیت آگهی امکان حذف آن وجود ندارد"))
        else:
            offers = Offer.objects.filter(packet=self)
            for offer in offers :
                offer.delete()
            super().delete(*args, **kwargs)

        
class Travel(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    departure = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="depar_country")
    departure_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="depar_city")
    destination = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="dest_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="dest_city")
    flight_date_start = models.DateField()
    flight_date_end = models.DateField(blank=True, null=True)
    visit_count = models.PositiveIntegerField(default=0) # This is useless. 
    offer_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    income = models.PositiveIntegerField(default=0)
    approved_packet = models.PositiveIntegerField(default=0)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True)
    status = models.IntegerField(choices=TRAVEL_STATUS, default=2)
    
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):

        #chack same country when packet is created
        if self.departure == self.destination:
            if self.departure_city == self.destination_city:
                raise PermissionDenied(detail="امکان یکی بودن مبدا و مقصد وجود ندارد")

        # Increase the travel_done number for user
        if self.status == 4:
            profile = Profile.objects.get(user=self.owner)
            profile.travel_done += 1
            profile.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Question is if a owner of travel wnats to delete it, what do we do ? TODO
        # when travel could be deleted then the all its offers should be deleted
        # if self.status == 3 and self.status == 4 and self.status == 8:
        if self.status == 2:
            offers = Offer.objects.filter(travel=self)
            for offer in offers :
                offer.delete()
            super().delete(*args, **kwargs)
        else:
            raise PermissionDenied(detail=_(".امکان حذف این سفر نیست"))
            

class Offer(BaseModel):
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, related_name="packet_ads")
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name="travel_ads")
    price = models.PositiveIntegerField()
    parcelPrice = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.CharField(default=generate_slug, max_length=8, unique=True, editable=False)
    status = models.IntegerField(choices=Offer, default=0)

    def __str__(self):
        return "%s --> %s" %(self.packet.owner,self.travel.owner)

    def delete(self, *args, **kwargs):
        disable_chat(self.slug)
        # Packet handling and change packet status if it is necessary
        self.packet.offer_count -= 1
        self.packet.save()
        if self.packet.offer_count == 0:
            self.packet.status = 0
            self.packet.save()

        # Travel handling and change travel status if it is necessary
        self.travel.offer_count -= 1
        self.travel.save()
        if self.travel.offer_count == 0:
            self.travel.status = 2
            self.travel.save()

        super().delete(*args, **kwargs)

    # What is defference between != and is not ? TODO
    def save(self, *args, **kwargs):
        # Check the new offer and increase offer_count of packet and travel by one due to packet status
        if self._state.adding:
            if self.packet.status == 3 or self.packet.status == 4 or self.packet.status == 5 or self.packet.status == 6 or self.packet.status == 7 :
                raise PermissionDenied(detail=_("با توجه به وضعیت آگهی امکان ثبت پیشنهاد وجود ندارد"))
            else:
                # Create chat when the offer is created.
                create_chat(self.slug, self.travel.owner, self.packet.owner, self.description)

                self.packet.offer_count += 1
                if self.packet.status == 0 :
                    self.packet.status = 1
                self.packet.save()
                self.travel.offer_count += 1
                self.travel.status = 3
                self.travel.save()
                super().save(*args, **kwargs)
        else:
            # Send the state of offer into chat, This is done for all state except new offer
            send_to_chat(self.status, self.slug)

            # Update packet state due to offer state
            if self.packet.status == 1:
                if (self.status != 1 and self.status is not 0): 
                    self.packet.status = self.status
                    self.packet.save()
                super().save(*args, **kwargs)
            else:
                if self.status != 1 and self.status is not 0: 
                    self.packet.status = self.status
                    self.packet.save()
                    super().save(*args, **kwargs)
            
            # When an offer reject by billiger this state is happend
                elif self.status == 1:
                    shouldPacketChange = False
                    packet = self.packet
                    offers = Offer.objects.filter(packet=packet)
                    for offer in offers:
                        if offer.status == 2:
                            shouldPacketChange = True
                    if shouldPacketChange:
                        self.packet.status = self.status
                        self.packet.save()
                    super().save(*args, **kwargs)

                # There is conflict here : income is consider for pay to traveler but pracel_price is not the 
                # income of treveler . so what should we do ?
                elif self.status == 3 :
                    self.travel.approved_packet += 1
                    if self.packet.buy:
                        self.travel.income += (self.price + self.parcel_price) 
                    else:
                        self.travel.income += self.price
                    self.travel.status = 3
                    self.travel.save()
                    super().save(*args, **kwargs)

                    # Here we check all the offers for a specific travel.
                # When an offer is done, we check others and
                # if all the others were done the state of travel should change to done.
                elif self.status == 6:
                    offers = Offer.objects.filter(travel=self.travel)
                    for offer in offers :
                        if (
                            offer.status == 0
                            or offer.status == 1 
                            or offer.status == 2
                            or offer.status == 3
                            or offer.status == 4
                            or offer.status == 5
                            ):
                            return None
                        else:
                            self.travel.status = 4
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
    def sender_slug(self):
        return self.travel.owner.slug
    
    @property
    def receiver_id(self):
        return self.packet.owner.id

    @property
    def receiver_slug(self):
        return self.packet.owner.slug
    
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
    
    @property
    def parcel_price_offer(self):
        return self.parcelPrice

    @property
    def buy(self):
        return self.packet.buy

    @property
    def travel_info(self):
        data = {
            "origin" : self.travel.departure.name,
            "origin_city" : self.travel.departure_city.name,
            "destination" : self.travel.destination.name,
            "destination_city" : self.travel.destination_city.name,
            "flight_date" : self.travel.flight_date_start
        }
        return data
    

class Bookmark(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bookmark_owner")
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, related_name="bookmark_packet")
    slug = models.CharField(default=generate_slug, max_length=8, unique=True, editable=False)

    def __str__(self):
        return str(self.packet.title)

    @property
    def packet_title(self):
        return str(self.packet.title)
    
    @property
    def packet_slug(self):
        return self.packet.slug

    @property
    def packet_picture(self):
        return self.packet.picture


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
    slug = models.CharField(default=generate_slug, max_length=8, unique=True, editable=False)

    def __str__(self):
        return str(self.id)
    
    # Compress the pic is done in frontend, is this here needed ? we can change the number to 200kb due to frontend TODO 
    def save(self, *args, **kwargs):
        MAX_FILE_SIZE = 10485760
        filesize = self.image_file.size
        if filesize > MAX_FILE_SIZE:
            raise ValidationError(detail=_("حجم تصویر بیش از حد زیاد است"))
        else:
            super().save(*args, **kwargs)


class Buyinfo(BaseModel):
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, related_name="packet_info")
    link = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.packet.title)


class Category(BaseModel):
    name = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='images/category')
    level = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)
