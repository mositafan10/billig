from rest_framework import serializers
from .models import Massage, Conversation
from account.serializers import UserSerializer


class MassageSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = Massage
        fields = ['text', 'owner']


class ConversationSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()
    sender = UserSerializer()
    class Meta:
        model = Conversation
        fields = ['receiver', 'sender','id']