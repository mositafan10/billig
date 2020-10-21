from redis import StrictRedis
import json


def add_notification(user_id, chat_id):
    r = StrictRedis(host='localhost', port=6379, db=0)
    r.hincrby('%s_notifications' % user_id, notification_id,)


def set_notification_as_read(user_id, notification_id):
    r = StrictRedis(host='localhost', port=6379)
    data = json.loads(r.hget('%s_notifications' % user_id, notification_id))
    data['read'] = True
    add_notification(user_id, notification_id, data)


def get_notifications(user_id):
    r = StrictRedis(host='localhost', port=6379)
    r   eturn r.hgetall('%s_notifications' % user_id)