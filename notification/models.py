from django.db import models
from users.models import User, Patient

# Create your models here.


class NotificationApp(models.Model):
    user_sender = models.ForeignKey(
        User, null=True, blank=True, related_name='user_sender', on_delete=models.CASCADE)
    user_receiver = models.ForeignKey(
        User, null=True, blank=True, related_name='user_receiver', on_delete=models.CASCADE)
    patient = models.ForeignKey(
        Patient, null=True, blank=True, related_name='patient', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=220, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
