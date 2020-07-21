from django.db import models
from django.db.models import Q
from account.models import User, BaseModel
from .utils import generate_slug



class ConversationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(sender='1')
 
 
class Conversation(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver")
    objects = models.Manager()
    chatlist = ConversationManager()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        count = Conversation.objects.filter(sender=self.sender, receiver=self.receiver).count()
        count1 = Conversation.objects.filter(sender=self.receiver, receiver=self.sender).count()
        if count == 0 and count1 == 0:
             super().save(*args, **kwargs)
        else:
            return None


class Massage(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="massage")
    text = models.TextField()
    chat_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return str(self.id)




