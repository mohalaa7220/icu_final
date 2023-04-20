from rest_framework import serializers
from .models import Medicines, Medicine
from users.models import Nurse, Doctor
from users.serializer import UsersPatientSerializer


class MedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields = ['id', 'name', 'created', 'updated']

    def validate(self, attrs):
        name = Medicines.objects.filter(name=attrs.get('name')).exists()
        if name:
            raise serializers.ValidationError(
                {'message': 'This name already exists'})
        return attrs


# Add to Nurse
class AddMedicineSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Nurse.objects.select_related('user'), many=True)

    class Meta:
        model = Medicine
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')
        patient = attrs.get('patient')
        if not name:
            raise serializers.ValidationError(
                {'message': 'This field name is required.'})
        if not patient:
            raise serializers.ValidationError(
                {'message': 'This field patient is required.'})
        return attrs


class ResultMedicineSerializer(serializers.ModelSerializer):
    nurse = UsersPatientSerializer(many=True, read_only=True)
    patient = serializers.StringRelatedField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Medicine
        exclude = ('doctor', )


class SimpleResultMedicineSerializer(serializers.ModelSerializer):
    nurse = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Medicine
        fields = '__all__'


class NurseResultMedicineSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Medicine
        exclude = ('nurse', )


# -------  Add Medicines for all Nurses
class AddAllNursesMedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        exclude = ('nurse', )
