from rest_framework import serializers
from .models import Massage, ChatID


class MassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massage
        fields = ['receiver','text','chat_id']


class ChatIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatID
        fields = ['receiver']