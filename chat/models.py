from django.db import models
from django.utils import timezone
from django.db.models import Q
from account.models import User, BaseModel, Profile
from advertise.models import Offer
from datetime import datetime
from core.utils import generate_slug
from core.constant import Massage_TYPE

 
class Conversation(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver")
    not_seen = models.PositiveIntegerField(default=4) # not completed
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True, primary_key=True) 

    def __str__(self):
        return str(self.slug)

    @property
    def receiver_name(self):
        return str(self.receiver.name)
    
    @property
    def sender_slug(self):
        return str(self.sender.slug)

    @property
    def receiver_slug(self):
        return str(self.receiver.slug)

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

    @property
    def packet_slug(self):
        return self.offer.packet.slug

    @property
    def packet_title(self):
        return self.offer.packet.title  


class Massage(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="massage")
    text = models.TextField(blank=True, null=True)
    picture = models.FileField(blank=True, null=True, upload_to='images/chat/%Y/%m')
    chat_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    first_day = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    type_text = models.IntegerField(choices=Massage_TYPE, default=0)

    def __str__(self):
        return str(self.id)

    @property
    def owner_name(self):
        return str(self.owner.name)

    @property
    def owner_slug(self):
        return self.owner.slug

    @property
    def owner_avatar(self): 
        user = self.owner
        profile = Profile.objects.get(user=user)
        return str(profile.picture)

    def save(self, *args, **kwargs):
        massages = Massage.objects.filter(chat_id=self.chat_id).order_by('-create_at')
        try:
            last_massage_date = massages[0].create_at
            self.chat_id.updated_at = datetime.now()
            self.chat_id.save()
            if (last_massage_date.date() != datetime.now().date()):
                self.first_day = True
        except:
            self.first_day = True
        super().save(*args, **kwargs)
    
  




