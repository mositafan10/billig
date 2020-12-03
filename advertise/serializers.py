from rest_framework import serializers
from .models import Packet, Travel, Offer, Bookmark, Report, PacketPicture, Buyinfo, Category
from account.serializers import CountrySerializer, CitySerializer, UserSerializer, ProfileSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','picture')

class PacketDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Packet
        fields = (
            'slug','title', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'category', 'category_other', 'buy',
            'weight','dimension', 'suggested_price', 'description','picture', 'status', 'owner_name', 'phonenumber_visible','no_matter_origin')


class PacketSerializer(serializers.ModelSerializer):
    origin_country = CountrySerializer()
    origin_city = CitySerializer()
    destination_country = CountrySerializer()
    destination_city = CitySerializer()
    status = serializers.CharField(source='get_status_display')
    category = CategorySerializer()
    dimension = serializers.CharField(source='get_dimension_display')
    
    class Meta:
        model = Packet
        fields = (
            'slug','title','owner_name','owner_slug','origin_country', 'origin_city', 'destination_country', 'destination_city', 'buy', 'phonenumber_visible','no_matter_origin',
            'category', 'dimension' ,'weight', 'suggested_price', 'description', 'picture', 'offer_count', 'create_at', 'status','parcel_price','parcel_link','phonenumber'
        )

class PacketSerializer1(serializers.ModelSerializer):
    destination_country = serializers.StringRelatedField()
    origin_city = serializers.StringRelatedField()
    origin_country = serializers.StringRelatedField()
    destination_city = serializers.IntegerField()
    category = serializers.IntegerField()
    status = serializers.StringRelatedField()
    class Meta:
        model = Packet
        fields = (
            'slug','title','owner_name', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'buy',
            'category','dimension','weight', 'suggested_price', 'description', 'offer_count', 'create_at', 'status','no_matter_origin',
        )

    
class TravelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Travel
        fields = (
            'slug', 'departure', 'departure_city', 'destination', 'destination_city', 'flight_date_start','flight_date_end',
            'description'
        )


class TravelDeserializer(serializers.ModelSerializer):
    departure = CountrySerializer()
    departure_city = CitySerializer()
    destination = CountrySerializer()
    destination_city = CitySerializer()
    
    class Meta:
        model = Travel
        fields = (
            'slug', 'departure', 'departure_city', 'destination', 'destination_city', 'flight_date_start','flight_date_end',
            'description', 'approved_packet', 'income', 'status','offer_count'
        )


class OfferSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Offer
        fields = ('slug','price','parcel_price','parcel_price_offer','status','description','sender','sender_slug','sender_avatar','receiver_avatar','receiver','receiver_slug','packet_slug', 'packet_title', 'buy', 'travel_info')


class OfferDeserializer(serializers.ModelSerializer):
    packet = serializers.StringRelatedField()
    travel = serializers.StringRelatedField()
    class Meta:
        model = Offer
        fields = ('packet', 'price', 'parcelPrice', 'travel', 'description')


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('packet',)

class BookmarkDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('slug','packet_slug','packet','packet_title','packet_picture')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('owner', 'packet', 'text')


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacketPicture
        fields = ('slug','image_file',)


class BuyinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyinfo
        fields = ('link','price')



