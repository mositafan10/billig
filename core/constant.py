#advertise_constant
TRAVEL_STATUS = [
        (0, "در انتظار تایید"),
        (1, "عدم تایید"),
        (2, "منتشر شده"),
        (3, "دارای بسته"),
        (4, "انجام شده"),
        (5, "حذف شده"),
        (6, "تسویه شده"),
        (7, "تسویه نشده"),
        (8, "در انتظار تسویه"),
] 

PACKET_STATUS = [
        (0, "منتشر شده"),
        (1, "دارای پیشنهاد"),
        (2, "در انتظار پرداخت"),
        (3, "در انتظار خرید"),
        (4, "در انتظار تحویل"),
        (5, "در انتظار تایید خریدار"),
        (6, "انجام شده"),
        (7, "تمام شده"),
        (8, "حذف شده"),
        (9, "منقضی شده"),
        (10, "در انتظار تایید"),
        (11, "عدم تایید"),
] 

Offer = [
        (0, "در انتظار پاسخ"), # default state
        (1, "در انتظار تایید مسافر"),# done by packet owner when accept offer : offer_update in advertise.view
        (2, "در انتظار پرداخت"), # done by traveler after confirm the price : offer_update in advertise.view
        (3, "در انتظار خرید"), # done after payment : verify function in payment.view
        (4, "در انتظار تحویل"),# done by traveler after buy parcel : offer_update function in advertise.view
        (5, "در انتظار تایید خریدار"), # done by traveler after get parcel in destination : offer_update function in advertise.view
        (6, "انجام شده"),# done by packet owner when receive parcel in destination : offer_update in advertise.view
        (7, "تمام شده"), # done after rating by packet owner in account.view
        (8, "حذف شده"), # done by offer owner : offer_update in advertise.view
] 

# for other choice we need a field to be filled by user about category TODO
PACKET_CATEGORY = [
        (0, "مدارک و مستندات"),
        (1, "کتاب و مجله"),
        (2, "لوازم الکترونیکی"),
        (3, "کفش و پوشاک"),
        (4, "لوازم آرایشی و بهداشتی"),
        (5, "دارو"),
        (6, "سایر موارد"),
]

DIMENSION = [
        (0, "کوچک"),
        (1, "متوسط"),
        (2, "بزرگ"),
]

#account_constant
Level = [
    ('1', 'Gold'),
    ('2', 'Silver'),
    ('3', 'Bronz'),
]

Social_Type = [
    ('0','Linkdin'),
    ('1','Facebook'),
    ('2','Instagram'),
    ('3','Twitter')
]


#chat_constant

Massage_TYPE = [
        (0,'p2p'),
        (1,'admin')
]

WelcomeText = "سلام . به بیلیگ پست خوش‌ آمدید. در اینجا می‌توانید سوالات خود را از ما بپرسید"