from rest_framework import serializers
from .models import Profile, Social, Score, CommentUser, Country, City, Follow, User


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','name']


class CitySerializer(serializers.ModelSerializer):
    # country = CountrySerializer()

    class Meta:
        model = City
        fields = ['id','name','country']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone_number','first_name']

        # def create(self, validated_data):
        #     user = super(UserSerializer, self).create(validated_data)
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     return user


class ProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # country = CountrySerializer()
    # city = CitySerializer()
    
    class Meta:
        model = Profile
        fields =  ['id','user','first_name','last_name','bio','picture','id_cart','country','city','birthday','favorite_gift','level','score','scores_count','comment_count','is_approved']


class SocialSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Social
        fields = ['id','user', 'title', 'social_id', 'is_approved']


class CommentUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CommentUser
        fields = ['id','owner', 'receiver', 'comment', 'is_approved']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'following']
