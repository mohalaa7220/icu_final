from rest_framework import serializers
from .models import NotificationApp


class NotificationSerializer(serializers.ModelSerializer):
    user_sender = serializers.StringRelatedField()

    class Meta:
        model = NotificationApp
        fields = '__all__'
