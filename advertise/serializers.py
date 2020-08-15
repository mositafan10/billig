from rest_framework import serializers
from .models import Packet, Travel, Offer, Bookmark, Report, PacketPicture
from account.serializers import CountrySerializer, CitySerializer, UserSerializer, ProfileSerializer


PACKET_CATEGORY = [
        (0, "مدارک و مستندات"),
        (1, "کتاب و مجله"),
        (2, "لوازم الکترونیکی"),
        (3, "کفش و پوشاک"),
        (4, "لوازم آرایشی و بهداشتی"),
        (5, "سایر موارد"),
]

class PacketDeserializer(serializers.ModelSerializer):
    # picture = serializers.ListField()

    class Meta:
        model = Packet
        fields = [
            'slug','title', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'category', 'buy',
            'weight', 'suggested_price', 'description','picture', 'status', 'owner_name'
        ]
    
    # def create(self, validated_data):

    #     images = validated_data.pop('picture')
    #     packet = Packet.objects.create(**validated_data)
    #     for image_id in images:
    #         try:
    #             # print(image_id)
    #             image = PacketPicture.objects.get(id=image_id)
    #             image.packet = packet
    #             image.save()
    #         except Exception as e:
    #             print('image not found with id={} , e= {}'.format(image_id, str(e)))
    #             pass
    #     return packet

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class PacketSerializer(serializers.ModelSerializer):
    destination_country = serializers.StringRelatedField()
    origin_city = serializers.StringRelatedField()
    origin_country = serializers.StringRelatedField()
    destination_city = serializers.StringRelatedField()
    status = serializers.CharField(source='get_status_display')
    category = serializers.CharField(source='get_category_display')
    
    class Meta:
        model = Packet
        fields = [
            'slug','title','owner_name', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'buy',
            'category', 'weight', 'suggested_price', 'description', 'picture', 'offer_count', 'create_at', 'status',
        ]

class PacketSerializer1(serializers.ModelSerializer):
    destination_country = serializers.StringRelatedField()
    origin_city = serializers.StringRelatedField()
    origin_country = serializers.StringRelatedField()
    destination_city = serializers.StringRelatedField()
    # category = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    class Meta:
        model = Packet
        fields = [
            'slug','title', 'owner_name', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'buy',
            'category', 'weight', 'suggested_price', 'description', 'picture', 'offer_count', 'create_at', 'status',
        ]

    
class TravelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Travel
        fields = [
            'slug', 'departure', 'departure_city', 'destination', 'destination_city', 'flight_date_start','flight_date_end',
            'description'
        ]


class TravelDeserializer(serializers.ModelSerializer):
    departure = serializers.StringRelatedField()
    departure_city = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()
    destination_city = serializers.StringRelatedField()

    class Meta:
        model = Travel
        fields = [
            'slug', 'departure', 'departure_city', 'destination', 'destination_city', 'flight_date_start','flight_date_end',
            'description'
        ]


class OfferSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Offer
        fields = ['slug','price','status','description','sender','sender_id','receiver','packet_slug']


class OfferDeserializer(serializers.ModelSerializer):
    packet = serializers.StringRelatedField()
    travel = serializers.StringRelatedField()
    # status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Offer
        fields = ['packet', 'price', 'travel', 'description']


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['owner', 'advertise']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['owner', 'packet', 'text']


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacketPicture
        fields = ['image_file']