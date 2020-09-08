from rest_framework import serializers
from .models import Profile, Score, Country, City, User


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','name','icon']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone_number','name']


class ProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()
    class Meta:
        model = Profile
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score 
        fields = ['score','text']

