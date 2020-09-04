from django.db import models
from account.models import BaseModel, User

class transaction(BaseModel):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user")
    amount = models.FloatField()
    transID = models.IntegerField()
    status = models.BooleanField()
    
    def __str__(self):
        return str(self.id)