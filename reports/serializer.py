from rest_framework import serializers
from .models import Nurse, DoctorReport, NurseReport, Doctor
from users.serializer import UsersPatientSerializer


class DoctorReportSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Nurse.objects.select_related('user'), many=True)

    class Meta:
        model = DoctorReport
        fields = ['title', 'nurse', 'patient']


class ResultDoctorReportSerializer(serializers.ModelSerializer):
    nurse = UsersPatientSerializer(many=True, read_only=True)
    patient = serializers.StringRelatedField()

    class Meta:
        model = DoctorReport
        fields = ['id', 'title', 'nurse', 'patient', 'created', 'updated']


class ResultDoctorReportAddedNurseSerializer(serializers.ModelSerializer):
    nurse = serializers.StringRelatedField(source='added_by')
    patient = serializers.StringRelatedField()

    class Meta:
        model = NurseReport
        fields = ['id', 'title', 'nurse', 'patient', 'created', 'updated']


# =================== Nurse ===========================================
class NurseReportSerializer(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Doctor.objects.all(), many=True)

    class Meta:
        model = NurseReport
        fields = ['title', 'doctor', 'patient']


class ResultNurseReportSerializer(serializers.ModelSerializer):
    doctor = UsersPatientSerializer(many=True, read_only=True)
    patient = serializers.StringRelatedField()

    class Meta:
        model = NurseReport
        fields = ['id', 'title', 'doctor', 'patient', 'created', 'updated']


class ResultNurseReportAddedDoctorSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField(source='added_by')
    patient = serializers.StringRelatedField()

    class Meta:
        model = DoctorReport
        fields = ['id', 'title', 'doctor', 'patient', 'created', 'updated']


# =================== Patient ===========================================
class ReportDoctorPatientSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Nurse.objects.all(), many=True)

    class Meta:
        model = DoctorReport
        fields = ['title', 'created', 'nurse', 'patient']


class ReportNursePatientSerializer(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Doctor.objects.all(), many=True)

    class Meta:
        model = NurseReport
        fields = ['title', 'created', 'doctor', "patient"]


class DoctorReportAllNursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorReport
        fields = ['title', 'patient']


class NurseReportAllDoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseReport
        fields = ['title', 'patient']
