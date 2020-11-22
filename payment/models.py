from django.db import models
from account.models import BaseModel, User
from advertise.models import Packet, Travel
from .utils import pay_to_traveler
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from core.utils import generate_slug




pay_status = [
    (0,'در انتظار تایید'),
    (1,'تایید پرداخت'),
    (2,'انجام شده'),
    (3,'انجام نشده'),
]

class Bank(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=24, blank=True, null=True, validators=[RegexValidator(regex=r'^\d{1,24}$', message=_("شماره شبا نامعتبر است")), RegexValidator(regex='^.{24}$',message=_("شماره شبا می‌بایست ۲۴ رقم باشد"))])
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.slug)


class TransactionReceive(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_packet")
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, related_name="travel")
    transId = models.BigIntegerField()
    amount = models.FloatField()
    status = models.BooleanField()
    factorNumber = models.CharField(max_length=8)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 
    
    def __str__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        self.packet.status = 3   # Change state to doing
        self.packet.save()
        super().save(*args, **kwargs)


class TransactionSend(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_travel")
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name="travel")
    amount = models.PositiveIntegerField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    status = models.IntegerField(choices=pay_status, default=0)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) 

    def __str__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        if self.status == 1:
            state = pay_to_traveler(self.user, self.amount, self.travel, self.bank.number)
            if state:
                self.status = 2
                self.travel.status = 6
                self.travel.save()
            else:
                self.status = 3
                self.travel.status = 7
                self.travel.save()
        super().save(*args, **kwargs)

