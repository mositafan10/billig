import random
import string
from .models import Massage, Conversation

def generate_slug():
    return ''.join(str(random.randint(0,9)) for _ in range(6))


def send_to_chat(status, chat_id):
    user = User.objects.get(pk=1)
    conversation = Conversation.objects.get(slug=chat_id)
    switcher = {
        1:"وضعیت پیشنهاد به «در انتظار تایید مسافر» تبدیل شده است.",
        2:"وضعیت پیشنهاد به « در انتظار پرداخت» تبدیل شده است.",
        3:"وضعیت پیشنهاد به «در انتظار خرید» تبدیل شده است.",
        4:"وضعیت پیشنهاد به «در انتظار تحویل» تبدیل شده است.",
        5:"وضعیت پیشنهاد به «در انتظار تایید خریدار» تبدیل شده است.",
        6:"وضعیت پیشنهاد به «انجام شده» تبدیل شده است.",
        7:"وضعیت پیشنهاد به «تمام شده» تبدیل شده است.",
    }
    text = switcher.get(status," ")
    Massage.objects.create(chat_id=conversation, type_text=1, text=text, owner=user)