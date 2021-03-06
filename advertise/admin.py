from account.models import City, Country
from django.contrib import admin, messages
from django.contrib.admin.decorators import register
from django.utils.translation import ngettext

from .models import *


@register(PacketPicture)
class PacketPictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug' ,'image_file','packet')
    
@register(Packet)
class PacketAdmin(admin.ModelAdmin):  
    list_display  = ('id','slug','title','owner_user','origin_country','destination_country',
                    'category','buy','get_pictures','weight','dimension','description','create_at','offer_count','visit_count','status')
    list_editable = ('status',)
    list_filter   = ('origin_country','category','create_at', 'status','dimension')
    raw_id_fields = ("owner",) 
    search_fields = ('owner___username','category')
    actions = ['make_approve']

    def owner_user(self, obj):
        return obj.owner.phone_number

    def get_pictures(self,obj):
        return obj.picture  
    
    def make_approve(self, request, queryset):
        updated = queryset.update(status=0)
        self.message_user(request, ngettext(
            '%d packet was successfully marked as approved.',
            '%d packets were successfully marked as approved.',
            updated,
        ) % updated, messages.SUCCESS)
    
    get_pictures.short_description  = "pictures" 
    make_approve.short_description = "Mark selected packets as approved"


@register(City)
class CityAdmin(admin.ModelAdmin):
    list_display  = ('id','name','country','is_active')
    list_filter   = ('country',)
    list_editable = ('is_active',)
    search_fields = ('name','country')


@register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id','name','city','is_active')
    list_editable = ('is_active',)
    
    def city(self,obj):
        cities = []
        for c in obj.city.all():
            cities.append(c)
        return cities
        

@register(Offer)       
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id','slug','packet','offer_owner','offer_to','origin','destination','price','suggested_price','parcelPrice','description','status')
    list_editable = ('status',)
     
    def offer_owner(self, obj):
        return obj.travel.owner.phone_number

    def offer_to(self, obj):
        return obj.packet.owner.phone_number
    
    def origin(self, obj):
        return obj.packet.origin_country

    def destination (self, obj):
        return obj.packet.destination_country

    def suggested_price (self, obj):
        return obj.packet.suggested_price 


@register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ('id','slug','owner_user','departure','destination','flight_date_start','flight_date_end','offer_count','status','create_at')
    list_editable = ('status',)
    list_filter = ('departure','destination',)
    search_fields = ('owner',)
    
    def owner_user(self, obj):
        return obj.owner.phone_number


@register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id','owner','packet')


@register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id','owner','packet','title','text','create_at')


@register(Buyinfo)
class BuyinfoAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'packet','price','currency','link')


@register(RemoveReason)
class RemoveReasonAdmin(admin.ModelAdmin):
    list_display = ( 'id','packet','type_remove', 'description')


@register(TravelRemoveReason)
class TravelRemoveReasonAdmin(admin.ModelAdmin):
    list_display = ( 'id','travel','type_remove', 'description')




