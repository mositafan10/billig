from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User, BaseModel, Country, City, Profile
from django.db import IntegrityError
from django.db import models
import random
import string

PACKET_STATUS = [
        ('0', 'در انتظار تایید'),
        ('1', 'عدم تایید'),
        ('2', 'منتشر شده'),
        ('3', 'دارای پیشنهاد'),
        ('4', 'پذیرش شده'),
        ('5', 'ارسال شده'),
] 

TRAVEL_STATUS = [
        ('0', 'در انتظار تایید'),
        ('1', 'عدم تایید'),
        ('2', 'منتشر شده'),
        ('3', 'دارای بسته'),
        ('4', 'پرواز کرد'),
] 

Offer = [
        ('0', 'در انتظار پاسخ'),
        ('1', 'تایید '),
        ('2', 'عدم تایید'),
] 


# for other choice we need a field to be filled by user about category TODO
PACKET_CATEGORY = [
        ('مدارک','0'),
        ('1', 'کتاب'),
        ('2','سایر موارد')
]

# CURRENCY = [
#         ('0','دلار'),('1','یورو'),('2','ریال'),
# ]

# Weight_Unit = [
#     ('0','گرم'),('1','کیلوگرم'),
# ]


def generate_slug():
    return ''.join(str(random.randint(0,9)) for _ in range(6))
    

class Packet(BaseModel):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(Profile, on_delete=models.PROTECT)
    origin_country = models.ForeignKey(Country, on_delete = models.PROTECT, related_name="origin_country")
    origin_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="origin_city")
    destination_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="destination_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="destination_city")
    category = models.CharField(max_length=20, choices=PACKET_CATEGORY)
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(30),MinValueValidator(1)])
    suggested_price = models.PositiveIntegerField()
    buy = models.BooleanField(default=False)
    picture = models.CharField(max_length=100 , blank=True, null=True) # need at most 3 picture TODO
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True) # should not be send by user: this should be validate
    status = models.CharField(max_length=20, choices=PACKET_STATUS, default=0)
    # weight_unit = models.CharField(max_length=5, choices=Weight_Unit)
    # currency = models.CharField(max_length=3, choices=CURRENCY)  
    # place_of_get = models.CharField(max_length=20 ,choices=PLACE) 
    # place_of_give = models.CharField(max_length=20 ,choices=PLACE)  
    # start_date = models.DateField()
    # end_date = models.DateField()
 
    def __str__(self):
        return str(self.id)

    def visit(self):
        self.visit_count += 1
        self.save()
    

class Travel(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    departure = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="depar_country")
    departure_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="depar_city")
    destination = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="dest_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="dest_city")
    empty_weight = models.PositiveIntegerField(validators=[MaxValueValidator(30),MinValueValidator(1)]) 
    flight_date = models.DateField() 
    slug = models.CharField(default=generate_slug, max_length=8, editable=False, unique=True, db_index=True)
    visit_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TRAVEL_STATUS, default='در انتظار تایید')
    # weight_unit = models.CharField(max_length=3, choices=Weight_Unit)
    
    def __str__(self):
        return str(self.id)
    
    def visit(self):
        self.visit_count += 1
        self.save()


class Offer(BaseModel):
    packet = models.ForeignKey(Packet, on_delete=models.PROTECT, related_name="packet_ads")
    travel = models.ForeignKey(Travel, on_delete=models.PROTECT, related_name="travel_ads")
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=3, choices=Offer, default='در انتظار پاسخ')
    # currency = models.CharField(max_length=3, choices=CURRENCY)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.packet.offer_count += 1
        self.packet.status = '2'   
        self.travel.offer_count += 1
        self.travel.status = '3'
        self.packet.save()
        self.travel.save()

class Bookmark(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="bookmark_owner")
    advertise = models.ForeignKey(Packet, on_delete=models.PROTECT, blank=True, null=True)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Report(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reporter")
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE)
    title = models.CharField(max_length=15)
    text = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s --> %s" %(self.owner,self.packet)


# class Ticket(BaseModel):
#     owner = models.ForeignKey(Profile, on_delete=models.PROTECT)
#     date = models.DateTimeField()
#     airline = models.CharField(max_length=40, choices=Airlines, blank=True,  null=True)
#     pic = models.FileField(blank=True,  null=True) #validate TODO
#     is_approved = models.BooleanField(default=False)

#     def __str__(self):
#         return "%s --> %s" %(self.owner, self.airline)

