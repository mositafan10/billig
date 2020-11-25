from rest_framework import serializers
from .models import TransactionReceive, TransactionSend, Bank

class TransactionReceiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionReceive
        fields = ('transId','amount','cardNumber','paymentDate','create_at')


class TransactionSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionSend
        fields = ('transId','amount','create_at')

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('name','number','slug')