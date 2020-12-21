from rest_framework import serializers
from .models import Massage, Conversation


class MassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massage
        fields = ('text','owner_name','owner_slug','create_at','owner_avatar','first_day','picture','is_seen','type_text')


class MassageDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Massage
        fields = ('text','picture')


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('slug','packet_title','receiver_name','sender_name','sender_slug','receiver_slug','receiver_avatar','sender_avatar','not_seen','is_active')


class ConversationDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('slug','receiver_slug')
