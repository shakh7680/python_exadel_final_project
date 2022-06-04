from pyfcm import FCMNotification
from django.conf import settings


def send_notification(user, message_title, message_body=None):
    push_service = FCMNotification(api_key=settings.FIREBASE_SECRET_KEY)
    result = push_service.notify_topic_subscribers(
        topic_name=user, sound=True, message_body=message_body, message_title=message_title
    )
    print(result)