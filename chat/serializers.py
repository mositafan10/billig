from rest_framework import serializers
from .models import Massage, Conversation
from account.serializers import UserSerializer


class MassageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Massage
        fields = ['text','owner_name','owner_slug','create_at','owner_avatar','first_day','picture']


class MassageDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Massage
        fields = ['text','picture']


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['slug','receiver_name','sender_name','sender_slug','receiver_slug','offer_state','receiver_avatar','sender_avatar','packet_slug','packet_title']


class ConversationDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['slug','receiver_slug']
