from rest_framework import serializers
from .models import NotificationApp


class NotificationSerializer(serializers.ModelSerializer):
    user_sender = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()

    class Meta:
        model = NotificationApp
        exclude = ('user_receiver',)
