from rest_framework import serializers
from .models import NotificationApp
from users.serializer import SimplePatientData, SimpleUserData


class NotificationSerializer(serializers.ModelSerializer):
    user_sender = SimpleUserData(read_only=True)
    user_receiver = SimpleUserData(read_only=True)
    patient = SimplePatientData(read_only=True)

    class Meta:
        model = NotificationApp
        fields = "__all__"


class NotificationHeadNursingSerializer(serializers.ModelSerializer):
    user_sender = SimpleUserData(read_only=True)
    user_receiver = SimpleUserData(read_only=True)
    patient = SimplePatientData(read_only=True)

    class Meta:
        model = NotificationApp
        fields = "__all__"
