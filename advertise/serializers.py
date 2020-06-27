from rest_framework import serializers
from .models import Packet, Travel, Offer, Bookmark, Report, PacketPicture
from account.serializers import CountrySerializer, CitySerializer, UserSerializer, ProfileSerializer


class PacketDeserializer(serializers.ModelSerializer):
    picture = serializers.ListField()
    
    class Meta:
        model = Packet
        fields = [
            'slug','title', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'category', 'buy',
            'weight', 'suggested_price', 'description','picture'
        ]
    
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

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class PacketSerializer(serializers.ModelSerializer):
    destination_country = serializers.StringRelatedField()
    origin_city = serializers.StringRelatedField()
    origin_country = serializers.StringRelatedField()
    destination_city = serializers.StringRelatedField()

    class Meta:
        model = Packet
        fields = [
            'slug','title', 'owner', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'buy',
            'category', 'weight', 'suggested_price', 'description', 'picture', 'offer_count', 'create_at', 'status',
        ]
    
class TravelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Travel
        fields = [
            'slug', 'departure', 'departure_city', 'destination', 'destination_city', 'flight_date', 'description'
        ]


class OfferSerializer(serializers.ModelSerializer):
    packet = serializers.StringRelatedField()
    # owner = serializers.StringRelatedField()
    class Meta:
        model = Offer
        fields = ['slug', 'owner', 'packet', 'price', 'flight_date', 'description']


class OfferDeserializer(serializers.ModelSerializer):
    packet = serializers.StringRelatedField()
    class Meta:
        model = Offer
        fields = ['slug', 'packet', 'price', 'flight_date', 'description']


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['owner', 'advertise']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['owner', 'packet', 'text']

