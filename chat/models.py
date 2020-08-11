from django.db import models
from django.db.models import Q
from account.models import User, BaseModel
from advertise.models import Offer
from .utils import generate_slug

 
 
class Conversation(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver")
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, related_name="offer")

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        count = Conversation.objects.filter(sender=self.sender, receiver=self.receiver).count()
        count1 = Conversation.objects.filter(sender=self.receiver, receiver=self.sender).count()
        if count == 0 and count1 == 0:
             super().save(*args, **kwargs)
        else:
            return None

    @property
    def receiver_name(self):
        return str(self.receiver.first_name + ' ' + self.receiver.last_name)

    @property
    def sender_name(self):
        return str(self.sender.first_name + ' ' + self.sender.last_name)
    
    @property
    def offer_state(self):
        return self.offer.get_status_display

    @property
    def sender_username(self):
        return str(self.sender.username)


class Massage(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="massage")
    text = models.TextField()
    chat_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return str(self.id)

    @property
    def owner_name(self):
        return str(self.owner.first_name + ' ' + self.owner.last_name)

    @property
    def ownerid(self):
        return self.owner.id


