from rest_framework import serializers
from .models import Profile, Score, Country, City, User, Newsletter, Social, CommentUser


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id','name','eng_name','icon')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id','name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('slug','phone_number','name')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('level','score','picture','name','travel_done','billlig_done','joined_at')

class PrivateProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()
    class Meta:
        model = Profile
        fields = ('phone_number','country','city','email','level','score','scores_count','comment_count','picture','name')

class ProfileDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('country','city','email','picture','name')


class LimitedProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('user', 'picture', 'country', 'score')


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score 
        fields = ('score','text','owner_avatar','owner_name','owner_slug','receiver_avatar','receiver_name','receiver_slug')


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('email',)


class SocialSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(source='get_account_type_display')
    class Meta:
        model = Social
        fields = ('slug','account_type','address')

class SocialDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ('account_type','address')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUser
        fields = ('owner','picture','name','text')

class CommentDeserializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUser
        fields = ('text',)