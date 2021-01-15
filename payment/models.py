from django.db import models
from account.models import BaseModel, User
from advertise.models import Offer
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
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.slug)


class TransactionReceive(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_packet")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offer_packet")
    transId = models.BigIntegerField()
    amount = models.FloatField()
    status = models.BooleanField()
    factorNumber = models.CharField(max_length=8)
    cardNumber = models.CharField(max_length=16)
    paymentDate = models.CharField(max_length=20)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True) 
    
    def __str__(self):
        return str(self.slug)
    
    @property
    def packetTitle(self):
        return self.offer.packet.title

    def save(self, *args, **kwargs):
        self.offer.packet.status = 3   # Change state to doing
        self.offer.packet.save()
        super().save(*args, **kwargs)


class TransactionSend(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_travel")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offer_travel")
    amount = models.PositiveIntegerField()
    transaction_id = models.CharField(max_length=15, null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    status = models.IntegerField(choices=pay_status, default=0)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True) 

    def __str__(self):
        return str(self.slug)

    @property
    def travelTitle(self):
        return '%s --> %s (%s)' %(self.offer.travel.departure, self.offer.travel.destination, self.offer.travel.flight_date_start)

    def save(self, *args, **kwargs):
        if self.status == 1:
            state = pay_to_traveler(self.user, self.amount, self.offer, self.bank.number, self.slug)
            # print("state", state)
            if state['status']:
                self.status = 2
                self.transaction_id = state['transaction_id']
                self.offer.travel.status = 6
                self.offer.travel.save()
            else:
                self.status = 3
                self.offer.travel.status = 7
                self.offer.travel.save()
        super().save(*args, **kwargs)

