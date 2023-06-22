from rest_framework import serializers
from .models import MedicalTest, Nurse, PatientMedicalImage, PatientRaysImage, Image
from users.serializer import UsersPatientSerializer
from django.core.exceptions import ValidationError


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
        fields = ['id', 'image_url', "image", 'created']

    def validate(self, attrs):
        if not attrs.get('image'):
            raise ValidationError({"message": "Image is required"})
        return super().validate(attrs)


class PatientRaysImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRaysImage
        fields = ['id', 'image_url', "image", 'created']

    def validate(self, attrs):
        if not attrs.get('image'):
            raise ValidationError({"message": "Image is required"})
        return super().validate(attrs)


class AddImageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Image
        fields = ('images',)


class ImageSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(source='url')

    class Meta:
        model = Image
        fields = ('id',  'images')

    def get_images(self, instance):
        return eval(instance.url) if instance.url else []
