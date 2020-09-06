from django.db import models
from account.models import BaseModel, User
from advertise.models import Packet, Travel


class TransactionReceive(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_packet")
    packet = models.ForeignKey(Packet, on_delete=models.PROTECT, related_name="travel")
    transId = models.IntegerField()
    amount = models.FloatField()
    status = models.BooleanField()
    factorNumber = models.IntegerField()
    
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.packet.status = '7'   # Change state to doing
        self.packet.save()
        super().save(*args, **kwargs)


class TransactionSend(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_travel")
    travel = models.ForeignKey(Travel, on_delete=models.PROTECT, related_name="travel")
    amount = models.IntegerField()
    status = models.BooleanField()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.travel.status = '6' # chango state to reward paid
        self.travel.save()
        super().save(*args, **kwargs)


