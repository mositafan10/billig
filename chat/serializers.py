from rest_framework import serializers
from .models import Massage, Conversation
from account.serializers import UserSerializer


class MassageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Massage
        fields = ['text', 'owner_name','ownerid','create_at','owner_avatar','first_day']


class MassageDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Massage
        fields = ['text', 'owner', 'chat_id']


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['receiver_name', 'sender_name','id','sender', 'offer_state', 'receiver_avatar', 'sender_avatar']


class ConversationDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id','receiver']
