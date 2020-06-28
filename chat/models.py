from django.db import models
from account.models import User, BaseModel

MASSAGE_TYPE = [
    ('0','text'),
    ('1','picture'),
    ('2','voice'),
]

class Massage(BaseModel):
    # need exact time with second
    # need for pic and voice upload in chat ?
    # need voice call for future without any number 
    # seperate massage in two gropy : packet and travel and different display
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver")
    text = models.TextField() # is that ok for saving other type in textfield ? savaing address !
    chat_id = models.PositiveIntegerField(null=True, blank=True) # for making group each conversation. is this needed ?

    def __str__(self):
        return "%s --> %s" %(self.sender, self.receiver)

