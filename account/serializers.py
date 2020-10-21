from rest_framework import serializers
from .models import Profile, Score, Country, City, User, Newsletter


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','name','eng_name','icon']


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
        fields = ['bio','country','city','email','favorite_gift','level','score','scores_count','comment_count','facebook_id','instagram_id','twitter_id','linkdin_id','account_number','picture','name']


class LimitedProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = [ 'user', 'picture', 'country', 'score']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score 
        fields = ['score','text','owner_avatar','owner_name']


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email']