from rest_framework import serializers
from .models import Massage, Conversation


class MassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massage
        fields = ['text','chat_id']


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['receiver', 'sender', 'chat_id']