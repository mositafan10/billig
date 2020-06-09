from rest_framework import serializers
from .models import Packet, Travel, Offer, Bookmark, Report, PacketPicture
from account.serializers import CountrySerializer, CitySerializer


class PacketDeserializer(serializers.ModelSerializer):
    # destination_country = serializers.StringRelatedField()
    # origin_city = serializers.StringRelatedField()
    # origin_country = serializers.StringRelatedField()
    # destination_city = serializers.StringRelatedField()
    picture = serializers.ListField()


    class Meta:
        model = Packet
        fields = ['id','title', 'owner', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'category', 'weight', 'suggested_price', 'description','picture']
    
    def create(self, validated_data):

        images = validated_data.pop('picture')
        packet = Packet.objects.create(**validated_data)
        for image_id in images:
            try:
                print(image_id)
                image = PacketPicture.objects.get(id=image_id)
                image.packet = packet
                image.save()
            except Exception as e:
                print('image not found with id={} , e= {}'.format(image_id, str(e)))
                pass
        return packet


class PacketSerializer(serializers.ModelSerializer):
    destination_country = serializers.StringRelatedField()
    origin_city = serializers.StringRelatedField()
    origin_country = serializers.StringRelatedField()
    destination_city = serializers.StringRelatedField()

    class Meta:
        model = Packet
        fields = ['id','title', 'owner', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'category', 'weight', 'suggested_price', 'description']
    
class TravelSerializer(serializers.ModelSerializer):
    # origin_country = CountrySerializer()
    # destination_country = CountrySerializer()
    # origin_city = CitySerializer()
    # destination_city = CitySerializer()

    class Meta:
        model = Travel
        fields = ['id','owner', 'departure', 'departure_city', 'destination', 'destination_city', 'empty_weight', 'flight_date', 'description']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['packet', 'travel', 'price', 'currency']


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['owner', 'advertise']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['owner', 'packet', 'text']

