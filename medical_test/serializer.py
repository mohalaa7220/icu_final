from rest_framework import serializers
from .models import MedicalTest, Nurse, PatientMedicalImage, PatientRaysImage
from users.serializer import UsersPatientSerializer


class DoctorMedicalSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalTest
        fields = ['name',  'patient']


class ResultDoctorMedicalSerializer(serializers.ModelSerializer):
    nurse = UsersPatientSerializer(many=True, read_only=True)
    patient = serializers.StringRelatedField()

    class Meta:
        model = MedicalTest
        fields = ['id', 'name', 'nurse', 'patient', 'created', 'updated']


class ResultPatientMedicalSerializer(serializers.ModelSerializer):
    nurse = UsersPatientSerializer(many=True, read_only=True)
    patient = serializers.StringRelatedField()
    doctor = serializers.StringRelatedField()

    class Meta:
        model = MedicalTest
        fields = ['id', 'name', 'doctor', 'nurse',
                  'patient', 'created', 'updated']


class PatientMedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedicalImage
        fields = ['image', 'created']


class PatientRaysImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRaysImage
        fields = ['image', 'created']
