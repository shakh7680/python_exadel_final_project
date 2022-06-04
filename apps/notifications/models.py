from django.db import models
from apps.account.models import CustomUser
from apps.order.models import Order
from apps.notifications.modules import send_notification


class Notification(models.Model):
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='company_notifications')
    notifier = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name="user_notifier")
    text = models.CharField(max_length=255, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        send_notification(user=self.company.id, message_body=self.text, message_title=None)
        super(Notification, self).save(*args, **kwargs)