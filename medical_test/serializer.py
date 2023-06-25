from rest_framework import serializers
from .models import MedicalTest, Nurse, PatientMedicalImage, PatientRaysImage, Image
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


class AddPatientMedicalImageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = PatientMedicalImage
        fields = ["images", 'name', 'patient']


class PatientMedicalImageSerializer(serializers.ModelSerializer):
    images_url = serializers.SerializerMethodField(source='url')
    patient = serializers.StringRelatedField()

    class Meta:
        model = PatientMedicalImage
        fields = ['id', "images_url", 'name', 'patient']

    def get_images_url(self, instance):
        return eval(instance.url) if instance.url else []


class AddPatientRaysImageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = PatientRaysImage
        fields = ["images", 'name', 'patient']


class PatientRaysImageSerializer(serializers.ModelSerializer):
    images_url = serializers.SerializerMethodField(source='url')
    patient = serializers.StringRelatedField()

    class Meta:
        model = PatientRaysImage
        fields = ['id', "images_url", 'name', 'patient']

    def get_images_url(self, instance):
        return eval(instance.url) if instance.url else []


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
