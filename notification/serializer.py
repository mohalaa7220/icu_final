from rest_framework import serializers
from .models import NotificationApp


class NotificationSerializer(serializers.ModelSerializer):
    user_sender = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()

    class Meta:
        model = NotificationApp
        exclude = ('user_receiver',)


class NotificationHeadNursingSerializer(serializers.ModelSerializer):
    user_sender = serializers.StringRelatedField()
    user_receiver = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()

    class Meta:
        model = NotificationApp
        fields = "__all__"
