from django.contrib import admin
from .models import Packet, Travel, Offer, Bookmark, Report, PacketPicture
from account.models import Country, City



class PacketAdmin(admin.ModelAdmin):
    list_display = ('id','slug','title','origin_country','destination_country',
                    'category','buy','description','create_at','visit_count','status')
    list_editable = ('status',)
    list_filter   = ('origin_country','category','create_at')
    raw_id_fields = ("owner",) 
    search_fields = ('owner___username','category')

    # def owner_user(self, obj):
    #     return obj.owner.user.id
    
class CityAdmin(admin.ModelAdmin):
    list_display  = ('id','name','country')
    list_filter   = ('country',)
    search_fields = ('name','country')

    # def packet_origin_city(self,obj):
    #     return obj.origin_city.count()

    # def packet_destination_city(self,obj):
    #     return obj.destination_city.count()

    # def travel_origin_city(self,obj):
    #     return obj.depar_city.count()

    # def travel_destination_city(self,obj):
    #     return obj.dest_city.count()

    # packet_origin_city.short_description = "po"
    # packet_destination_city.short_description = "pd"
    # travel_origin_city.short_description = "to"
    # travel_destination_city.short_description = "td"

class CountryAdmin(admin.ModelAdmin):
    list_display = ('id','name','city')
    
    def city(self,obj):
        cities = []
        for c in obj.city.all():
            cities.append(c)
        return cities

    # def packet_origin_country(self,obj):
    #     return obj.origin_country.count()

    # def packet_destination_country(self,obj):
    #     return obj.destination_country.count()

    # def travel_origin_country(self,obj):
    #     return obj.depar_country.count()

    # def travel_destination_country(self,obj):
    #     return obj.dest_country.count()

    # packet_origin_country.short_description = "po"
    # packet_destination_country.short_description = "pd"
    # travel_origin_country.short_description = "to"
    # travel_destination_country.short_description = "td"
         
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id','origin','destination','price','suggested_price','description')

    # def Offer_owner(self, obj):
    #     return obj.travel.owner.user

    # def Offer_to(self, obj):
    #     return obj.packet.owner.user
    
    def origin (self, obj):
        return obj.packet.origin_country

    def destination (self, obj):
        return obj.packet.destination_country

    def suggested_price (self, obj):
        return obj.packet.suggested_price 


class TravelAdmin(admin.ModelAdmin):
    list_display = ('id','slug','owner_user','departure','destination','flight_date','empty_weight','visit_count','status','create_at')
    list_editable = ('status',)
    list_filter = ('departure','destination',)
    search_fields = ('owner',)
    
    def owner_user(self, obj):
        return obj.owner.user


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('owner','advertise','travel')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('owner','packet','text','create_at')

class PacketPictureAdmin(admin.ModelAdmin):
    list_display = ('id','image_file','packet')


admin.site.register(Packet, PacketAdmin)
admin.site.register(Travel, TravelAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(PacketPicture,PacketPictureAdmin)

