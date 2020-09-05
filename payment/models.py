from django.db import models
from account.models import BaseModel, User
from advertise.models import Packet, Travel

class TransactionReceive(BaseModel):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user")
    packet = models.ForeignKey(Packet, on_delete=models.PROTECT, related_name="travel")
    transID = models.IntegerField()
    amount = models.FloatField()
    status = models.BooleanField()
    
    def __str__(self):
        return str(self.id)

class TransactionSend(BaseModel):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user")
    travel = models.ForeignKey(Travel, on_delete=models.PROTECT, related_name="travel")
    amount = models.IntegerField()
    status = models.BooleanField()