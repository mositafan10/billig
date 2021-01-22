import json
import string

from account.models import BaseModel, City, Country, Profile, User
from chat.utils import create_chat, disable_chat, send_admin_text, send_to_chat
from core.constant import (Currency, Dimension, OfferChoices, OfferStatus,
                           PacketStatus, PacketType, RemoveChoices,
                           ReportChoices, TravelRemoveReason, TravelStatus,
                           Weight)
from core.utils import generate_slug, send_sms_packet
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import IntegrityError, models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied, ValidationError


# We can add type fild for future. For example gift type. TODO
class Packet(BaseModel):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    origin_country = models.ForeignKey(Country, on_delete = models.PROTECT, related_name="origin_country", null=True, blank=True)
    origin_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="origin_city", null=True, blank=True)
    no_matter_origin = models.BooleanField(default=False) 
    destination_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="destination_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="destination_city")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="category")
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name="sub_category", null=True, blank=True)
    weight = models.IntegerField(choices=Weight)
    dimension = models.IntegerField(choices=Dimension)
    suggested_price = models.PositiveIntegerField(default=0)
    buy = models.BooleanField(default=False)
    picture = models.CharField(default=1, max_length=8)
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=1000)
    slug = models.CharField(default=generate_slug, max_length=10, editable=False, unique=True)
    is_real = models.BooleanField(default=True)
    topic = models.IntegerField(choices=PacketType, default=0)
    status = models.IntegerField(choices=PacketStatus, default=0)
    
 
    def __str__(self):
        return '%s - %s - %s' %(self.id, self.slug, self.title)
    
    @property
    def owner_name(self):
        return str(self.owner.name)

    @property
    def owner_slug(self):
        return str(self.owner.slug)

    @property
    def buyinfo(self):
        data = {
            "currency":self.packet_info.get().currency,
            "link":self.packet_info.get().link,
            "price":self.packet_info.get().price
        }
        return data

    def save(self, *args, **kwargs):
        
        # Send admin text while create packet   
        if self._state.adding:
            send_admin_text(self.status, self.title, self.owner)

             # Different slug for buy and post packet
            if self.buy:
                self.slug = 'b%s' %(self.slug)
            else:
                self.slug = 'p%s' %(self.slug)

        # Check same country when packet is created
        if self.origin_country == self.destination_country:
            if self.origin_city == self.destination_city:
                raise PermissionDenied(detail=_("امکان یکی بودن مبدا و مقصد وجود ندارد"))
        
        # Send admin text
        if self.status == 10 or self.status == 11:
            # send_admin_text(self.status, self.title, self.owner)
            pass
        
        # Increase number of billlig_done by user
        if self.status == 7:
            profile = Profile.objects.get(user=self.owner)
            profile.billlig_done += 1
            profile.save()

        super().save(*args, **kwargs)
    
    # Question is if a owner of packet wnats to delete it, what do we do ? TODO
    # Check the correct error on frontend
    # when packet could be deleted then the all its offers should be deleted
    def delete(self, *args, **kwargs):
        if self.status == 3 or self.status == 4 or self.status == 5 or self.status == 6 :
            raise PermissionDenied(detail=_("تا زمانی که آگهی شما پیشنهاد دارد، امکان حذف وجود ندارد"))
        else:
            offers = Offer.objects.filter(packet=self).exclude(status=8)
            for offer in offers :
                offer.delete()
            super().save(*args, **kwargs)

        
class Travel(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    departure = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="depar_country")
    departure_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="depar_city")
    destination = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="dest_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="dest_city")
    flight_date_start = models.DateField()
    flight_date_end = models.DateField(blank=True, null=True)
    offer_count = models.PositiveIntegerField(default=0)
    income = models.PositiveIntegerField(default=0)
    approved_packet = models.PositiveIntegerField(default=0)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True)
    status = models.IntegerField(choices=TravelStatus, default=2)
    
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
        if self.status == 2:
            # travel = Travel.objects.get(slug=self.slug)
            # try:
            #     offers = Offer.objects.filter(travel=travel)
            #     for offer in offers :
            #         print(offer)
            #         offer.delete()
            # except expression as identifier:
            #     pass
            super().delete(args, **kwargs)
        else:
            raise PermissionDenied(detail=_("تا زمانی که سفر شما پیشنهاد دارد امکان حذف  سفر وجود ندارد."))
            

class Offer(BaseModel):
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, related_name="packet_ads")
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name="travel_ads")
    price = models.PositiveIntegerField()
    parcelPrice = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.CharField(default=generate_slug, max_length=8, unique=True, editable=False)
    status = models.IntegerField(choices=OfferStatus, default=0)
    offer_type = models.IntegerField(choices=OfferChoices, default=0)

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

        super().save(*args, **kwargs)
        # super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Check the new offer and increase offer_count of packet and travel by one due to packet status
        if self._state.adding:
            if self.packet.status == 3 or self.packet.status == 4 or self.packet.status == 5 or self.packet.status == 6 or self.packet.status == 7 :
                raise PermissionDenied(detail=_("با توجه به وضعیت آگهی امکان ثبت پیشنهاد وجود ندارد"))
            else:
                send_sms_packet(self.packet.owner.phone_number, self.packet, "offer")
                self.packet.offer_count += 1
                if self.packet.status == 0 :
                    self.packet.status = 1
                self.packet.save()
                self.travel.offer_count += 1
                self.travel.status = 3
                self.travel.save()
                super().save(*args, **kwargs)

                # Create chat when the offer is created.
                create_chat(self, self.slug, self.travel.owner, self.packet.owner, self.description)
        else:
            # Send the state of offer into chat, This is done for all state except new offer
            send_to_chat(self.status, self.slug, self.packet.status, self.packet.buy)

            # Update packet state due to offer state
            if self.packet.status == 1:
                if (self.status != 1 and self.status != 0): 
                    self.packet.status = self.status
                    self.packet.save()
                super().save(*args, **kwargs)
            else:
                if self.status != 1 and self.status != 0: 
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
    def packet_picture(self):
        return self.packet.picture

    @property
    def packet_category(self):
        return (self.packet.category)                                                                      

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
    title = models.IntegerField(choices=ReportChoices)
    text = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s --> %s" %(self.owner,self.packet)


class PacketPicture(BaseModel):
    image_file = models.FileField(upload_to='images/%Y/%m',validators=[FileExtensionValidator(allowed_extensions=['png,jpg'])])
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
    link = models.CharField(max_length=200, null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=5, choices=Currency, default="تومان")
    slug = models.CharField(default=generate_slug, max_length=8, unique=True, editable=False)

    def __str__(self):
        return str(self.packet.title)


class Category(BaseModel):
    name = models.CharField(max_length=30)
    eng_name = models.CharField(max_length=30)
    picture = models.FileField(upload_to='images/category')
    fee = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class SubCategory(BaseModel):
    name = models.CharField(max_length=30)
    eng_name = models.CharField(max_length=30)
    categoty = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class RemoveReason(BaseModel):
    packet = models.ForeignKey(Packet, on_delete=models.Case)
    type_remove = models.IntegerField(choices=RemoveChoices)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.packet.title


class TravelRemoveReason(BaseModel):
    travel = models.ForeignKey(Travel, on_delete=models.Case)
    type_remove = models.IntegerField(choices=TravelRemoveReason)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.travel.title