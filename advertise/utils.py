from chat.models import Massage, Conversation
from account.models import User
from core.utils import send_chat_notification

def send_to_chat(status, chat_id):
    user = User.objects.get(pk=1)
    conversation = Conversation.objects.get(slug=chat_id)
    switcher = {
        1:"وضعیت پیشنهاد به «در انتظار تایید مسافر» تبدیل شد.",
        2:"وضعیت پیشنهاد به «در انتظار پرداخت» تبدیل شد.",
        3:"وضعیت پیشنهاد به «در انتظار خرید» تبدیل شد.",
        4:"وضعیت پیشنهاد به «در انتظار تحویل» تبدیل شد.",
        5:"وضعیت پیشنهاد به «در انتظار تایید خریدار» تبدیل شد.",
        6:"وضعیت پیشنهاد به «انجام شده» تبدیل شد.",
        7:"وضعیت پیشنهاد به «تمام شده» تبدیل شد.",
    }
    text = switcher.get(status," ")
    Massage.objects.create(chat_id=conversation, type_text=1, text=text, owner=user)
    # send_chat_notification(conversation.receiver, 2)


def send_admin_text(status, packet, receiver):
    admin = User.objects.get(pk=1)
    conversation = Conversation.objects.get(sender=admin, receiver=receiver)
    switcher = {
        0 : "آگهی {} منتشر شد. این آگهی به مدت یک ماه بر روی سایت قرار خواهد گرفت".format(packet),
        10 : "آگهی {} در انتظار تایید است. خواهشمندیم منتظر بمانید.".format(packet),
        11 : "آگهی {} به دلیل عدم مطابقت با سیاست‌های بیلیگ منتشر نشد.".format(packet),
    }
    text = switcher.get(status," ")
    Massage.objects.create(chat_id=conversation, type_text=0, text=text, owner=admin)


