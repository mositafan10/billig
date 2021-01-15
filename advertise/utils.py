# from chat.models import Massage, Conversation
# from account.models import User
# from core.utils import send_chat_notification, send_sms_publish, send_sms_notpublish

# def send_to_chat(status, chat_id, packet_status, buy):
#     user = User.objects.get(pk=1)
#     conversation = Conversation.objects.get(slug=chat_id)
#     switcher_post = {
#         1:"وضعیت پیشنهاد به «در انتظار تایید مسافر» تغییر کرد.",
#         2:"وضعیت پیشنهاد به «در انتظار پرداخت» تغییر کرد.",
#         3:"وضعیت پیشنهاد به «در انتظار دریافت» تغییر کرد.",
#         4:"وضعیت پیشنهاد به «در انتظار تحویل» تغییر کرد.",
#         5:"وضعیت پیشنهاد به «در انتظار تایید بیلیگر» تغییر کرد.",
#         6:"وضعیت پیشنهاد به «انجام شده» تغییر کرد.",
#         7:"وضعیت پیشنهاد به «تمام شده» تغییر کرد.",
#         8:"پیشنهاد حذف شد.",
#     }
#     switcher_buy = {
#         1:"وضعیت پیشنهاد به «در انتظار تایید مسافر» تغییر کرد.",
#         2:"وضعیت پیشنهاد به «در انتظار پرداخت» تغییر کرد.",
#         3:"وضعیت پیشنهاد به «در انتظار خرید» تغییر کرد.",
#         4:"وضعیت پیشنهاد به «در انتظار تحویل» تغییر کرد.",
#         5:"وضعیت پیشنهاد به «در انتظار تایید بیلیگر» تغییر کرد.",
#         6:"وضعیت پیشنهاد به «انجام شده» تغییر کرد.",
#         7:"وضعیت پیشنهاد به «تمام شده» تغییر کرد.",
#         8:"پیشنهاد حذف شد.",
#     }
#     if buy:
#         text = switcher_buy.get(status," ")
#     else:
#         text = switcher_post.get(status," ")
#     Massage.objects.create(chat_id=conversation, type_text=1, text=text, owner=user)


# def send_admin_text(status, packet, receiver):
#     admin = User.objects.get(pk=1)
#     conversation = Conversation.objects.get(sender=admin, receiver=receiver)
#     switcher = {
#         0 : "آگهی {} منتشر شد. این آگهی به مدت یک ماه بر روی سایت باقی خواهد ماند".format(packet),
#         10 : "آگهی {} در انتظار تایید است. خواهشمندیم منتظر بمانید.".format(packet),
#         11 : "آگهی {} به دلیل عدم مطابقت با قوانین بیلیگ منتشر نشد.".format(packet),
#     }
#     text = switcher.get(status," ")
#     Massage.objects.create(chat_id=conversation, type_text=0, text=text, owner=admin)
#     if status == 0:
#         try:
#             pass
#             send_sms_publish(receiver.phone_number, packet)
#         except:
#             pass # What should we do here ? TODO
#     elif status == 11:
#         try:
#             pass
#             send_sms_notpublish(receiver.phone_number, packet)
#         except:
#             pass # What should we do here ? TODO

# def disable_chat(slug):
#     conversation = Conversation.objects.get(slug=slug)
#     conversation.is_active = False
#     conversation.save()


# def create_chat(slug,sender,receiver,text):
#     conversation = Conversation.objects.create(slug=slug, sender=sender, receiver=receiver)
#     Massage.objects.create(owner=conversation.sender, text=text, first_day=True, chat_id=conversation )




