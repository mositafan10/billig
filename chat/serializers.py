from rest_framework import serializers
from .models import Massage


class MassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massage
        fields = ['sender','receiver','mtype','text','chat_id']