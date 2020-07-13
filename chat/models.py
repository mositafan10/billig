from django.db import models
from account.models import User, BaseModel
from .utils import generate_slug

 
class ChatID(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver")
    chat_id = models.CharField(default=generate_slug(), max_length=8, editable=False, unique=True)
    
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        count = ChatID.objects.filter(sender=self.sender, receiver=self.receiver).count()
        if count == 0 :
             super().save(*args, **kwargs)
        else:
            return None


class Massage(BaseModel):
    text = models.TextField()
    chat_id = models.ForeignKey(ChatID, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)



