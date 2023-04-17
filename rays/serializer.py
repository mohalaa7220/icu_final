from rest_framework import serializers
from .models import Rays, Nurse
from users.serializer import UsersPatientSerializer


class DoctorRaysSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Nurse.objects.select_related('user'), many=True)

    class Meta:
        model = Rays
        fields = ['name', 'nurse', 'patient']


class ResultDoctorRaysSerializer(serializers.ModelSerializer):
    nurse = UsersPatientSerializer(many=True, read_only=True)
    patient = serializers.StringRelatedField()

    class Meta:
        model = Rays
        fields = ['id', 'name', 'nurse', 'patient', 'created', 'updated']


class ResultPatientRaysSerializer(serializers.ModelSerializer):
    nurse = UsersPatientSerializer(many=True, read_only=True)
    patient = serializers.StringRelatedField()
    doctor = serializers.StringRelatedField()

    class Meta:
        model = Rays
        fields = ['id', 'name', 'doctor', 'nurse',
                  'patient', 'created', 'updated']
