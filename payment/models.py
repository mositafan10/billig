from django.db import models
from account.models import BaseModel, User
from advertise.models import Packet, Travel
from .utils import pay_to_traveler

pay_status = [
    (0,'در انتظار تایید'),
    (1,'تایید پرداخت'),
    (2,'انجام شده'),
    (3,'انجام نشده'),

]

class TransactionReceive(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_packet")
    packet = models.ForeignKey(Packet, on_delete=models.PROTECT, related_name="travel")
    transId = models.BigIntegerField()
    amount = models.FloatField()
    status = models.BooleanField()
    factorNumber = models.IntegerField()
    
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.packet.status = 3   # Change state to doing
        self.packet.save()
        super().save(*args, **kwargs)


class TransactionSend(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_travel")
    travel = models.ForeignKey(Travel, on_delete=models.PROTECT, related_name="travel")
    amount = models.PositiveIntegerField()
    status = models.IntegerField(choices=pay_status, default=0)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.status == 2:
            state = pay_to_traveler(self.user, self.amount, self.travel)
            if state:
               self.status == 3
            else:
               self.status == 4
        super().save(*args, **kwargs)

