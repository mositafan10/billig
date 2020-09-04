from django.db import models
from django.db.models import Q
from account.models import User, BaseModel, Profile
from advertise.models import Offer
from .utils import generate_slug
from datetime import datetime

 
class Conversation(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offer")
    
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            count = Conversation.objects.filter(offer=self.offer).count()
            if (count == 0): 
                super().save(*args, **kwargs)
            else:
                return None
        else:
            super().save(*args, **kwargs)
            return self.id

    @property
    def receiver_name(self):
        return str(self.receiver.name)

    @property
    def sender_name(self):
        return str(self.sender.name)
        
    @property
    def offer_state(self):
        return self.offer.get_status_display

    @property
    def sender_username(self):
        return str(self.sender.username)

    @property
    def sender_avatar(self):
        user = self.sender
        profile = Profile.objects.get(user=user)
        return str(profile.picture)

    @property
    def receiver_avatar(self):
        user = self.receiver
        profile = Profile.objects.get(user=user)
        return str(profile.picture)


class Massage(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="massage")
    text = models.TextField()
    chat_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    first_day = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def owner_name(self):
        return str(self.owner.name)

    @property
    def ownerid(self):
        return self.owner.id

    @property
    def owner_avatar(self): 
        user = self.owner
        profile = Profile.objects.get(user=user)
        return str(profile.picture)

    def save(self, *args, **kwargs):
        massages = Massage.objects.filter(chat_id=self.chat_id).order_by('-create_at')
        count = massages.count()
        if count != 0 :
            last_massage_date = massages[0].create_at
        else :
            self.first_day = True

        self.chat_id.updated_at = datetime.now()
        self.chat_id.save()
        super().save(*args, **kwargs)
        if ( count != 0):
            if (last_massage_date.date() != self.create_at.date()):
                self.first_day = True
                self.save() 
    
  




