from rest_framework import serializers
from .models import TransactionReceive

class TransactionReceiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionReceive
        fields = ['transId','amount','create_at']