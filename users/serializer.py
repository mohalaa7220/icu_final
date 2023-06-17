from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import (Admin, User, Doctor, Nurse, Patient)
from rest_framework.response import Response


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "phone"]

    def validate(self, attrs):
        user = self.context['request'].user
        phone_exists = User.objects.exclude(
            pk=user.pk).filter(phone=attrs["phone"]).exists()
        email_exists = User.objects.exclude(
            pk=user.pk).filter(email=attrs["email"]).exists()
        if phone_exists:
            raise ValidationError({"message": "Phone has already been used"})
        if email_exists:
            raise ValidationError({"message": "email has already been used"})

        return super().validate(attrs)


# --------- User Serializer
class UserSerializer(serializers.ModelSerializer):
    added_by = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "name", "phone", "added_by", 'address', 'status',
                  'nat_id', 'image', 'specialization', "role",  "gender", "age"]


# --------- Simple User Serializer
class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "name", "phone"]


# --------- SignUp Admin Serializer
class SignUpAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "name", "phone", "password"]

    extra_kwargs = {
        'email': {'required': True},
        'username': {'required': True},
        'name': {'required': True},
        'phone': {'required': True},
        'password': {'required': True},
    }

    def validate(self, attrs):
        phone_exists = User.objects.filter(phone=attrs["phone"]).exists()
        if phone_exists:
            raise ValidationError({"message": "Phone has already been used"})

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data['role'] = 'admin'

        if validated_data['role'] == 'admin':
            validated_data['is_admin'] = True
            validated_data['is_staff'] = True
            validated_data['is_superuser'] = True
            validated_data['is_active'] = False

        user = super().create(validated_data)
        user.set_password(password)

        if user.is_admin == True:
            user.save()
            Admin.objects.create(user=user)
        user.save()
        return user


# --------- SignUp Serializer
class SignUpUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "name", "phone", 'image', 'nat_id', 'address', 'status',
                  "password", "role", "gender", "age", "specialization"]

        extra_kwargs = {
            'role': {'required': True},
        }

    def validate(self, attrs):
        phone_exists = User.objects.filter(phone=attrs["phone"]).exists()
        nat_exists = User.objects.filter(nat_id=attrs["nat_id"]).exists()

        if phone_exists:
            raise ValidationError({"message": "Phone has already been used"})
        if nat_exists:
            raise ValidationError({"message": "ID must be unique"})
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        if validated_data['role'] == 'doctor':
            validated_data['is_doctor'] = True

        elif validated_data['role'] == 'nurse':
            validated_data['is_nurse'] = True

        elif validated_data['role'] == 'headnursing':
            existing_headnursing = User.objects.filter(
                is_headnursing=True).first()

            if existing_headnursing:
                raise ValidationError(
                    {"message": "Only one head nursing account is allowed."})

            validated_data['is_headnursing'] = True

        user = super().create(validated_data)
        user.set_password(password)

        if user.is_doctor == True:
            Doctor.objects.create(user=user)
            user.save()

        if user.is_nurse == True:
            Nurse.objects.create(user=user)
            user.save()

        user.save()
        return user


# Add Nurse to doctor
class AddNurseSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        queryset=Nurse.objects.all(), many=True, slug_field='user_id')
    doctor = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='id')

    class Meta:
        model = Doctor
        fields = ["doctor", "nurse"]


# Return Nurses User
class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = ["user"]

    def to_representation(self, instance):
        return SimpleUserSerializer(instance.user).data


# Return Doctor User
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["user"]

    def to_representation(self, instance):
        return SimpleUserSerializer(instance.user).data


# Updated Profile
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "name", 'address', 'status',
                  "phone", "role", "gender", "age"]

        def validate(self, value):
            user = self.context['request'].user
            if User.objects.exclude(pk=user.pk).filter(email=value).exists():
                raise serializers.ValidationError(
                    {"email": "This email is already in use."})

            if User.objects.exclude(pk=user.pk).filter(username=value).exists():
                raise serializers.ValidationError(
                    {"username": "This username is already in use."})
            return value

        def update(self, instance, validated_data):
            user = self.context['request'].user

            if user.pk != instance.pk:
                raise serializers.ValidationError(
                    {"authorize": "You dont have permission for this user."})

            instance.name = validated_data['name']
            instance.email = validated_data['email']
            instance.username = validated_data['username']
            instance.save()

            return instance


# --------- Add Patient
class AddPatient(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(
        queryset=Doctor.objects.select_related('user'), many=True, slug_field='user_id')
    nurse = serializers.SlugRelatedField(
        queryset=Nurse.objects.select_related('user'), many=True, slug_field='user_id')

    class Meta:
        model = Patient
        fields = ["name", "image", "doctor", 'nurse', 'address',
                  'disease_type', 'room_number', 'nat_id', 'phone', 'gender', 'age', 'status']

    def validate(self, attrs):
        phone_exists = Patient.objects.filter(phone=attrs["phone"]).exists()
        nat_exists = Patient.objects.filter(nat_id=attrs["nat_id"]).exists()

        if phone_exists:
            raise ValidationError({"message": "Phone has already been used"})
        if nat_exists:
            raise ValidationError({"message": "ID must be unique"})
        return super().validate(attrs)

    def create(self, validated_data):
        patient = super().create(validated_data)
        patient.save()
        return patient


class UpdatePatientProfileSerializer(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(
        queryset=Doctor.objects.select_related('user'), many=True, slug_field='user_id')
    nurse = serializers.SlugRelatedField(
        queryset=Nurse.objects.select_related('user'), many=True, slug_field='user_id')

    class Meta:
        model = Patient
        fields = ["name", "image", "doctor", 'nurse', 'address',
                  'disease_type', 'room_number', 'nat_id', 'phone', 'gender', 'age', 'status']

    def validate(self, attrs):
        patient = self.context.get('patient')
        phone_exists = Patient.objects.exclude(
            pk=patient.pk).filter(phone=attrs["phone"]).exists()
        nat_exists = Patient.objects.exclude(
            pk=patient.pk).filter(nat_id=attrs["nat_id"]).exists()

        if phone_exists:
            raise serializers.ValidationError("Phone has already been used.")
        if nat_exists:
            raise serializers.ValidationError("ID must be unique.")
        return attrs


class UsersPatientSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='user.id')
    name = serializers.CharField(source='user.name')
    phone = serializers.CharField(source='user.phone')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Nurse
        fields = ['id', 'name', 'phone', 'email']


# Patient ---------
class PatientSerializer(serializers.ModelSerializer):
    nurse = UsersPatientSerializer(many=True, read_only=True)
    doctor = UsersPatientSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'name', 'image',  'disease_type', 'room_number', 'address',
                  'nat_id', 'phone', 'gender', 'age', 'status', 'doctor', 'nurse']


# ----- Return Patient for doctor and nurse
class PatientDoctorsSerializer(serializers.ModelSerializer):
    user = UsersPatientSerializer(many=True, read_only=True, source='nurse')

    class Meta:
        model = Patient
        fields = ['id', 'name', 'image', 'disease_type', 'room_number', 'address',
                  'phone',  'age', 'status', 'user']


# ----- Return Patient for doctor and nurse
class PatientNurseSerializer(serializers.ModelSerializer):
    user = UsersPatientSerializer(many=True, read_only=True, source='doctor')

    class Meta:
        model = Patient
        fields = ['id', 'name', 'image', 'disease_type', 'room_number',
                  'phone',  'age', 'status', 'user']


class UsersName(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# ============================================================================
# Reset Password
# ============================================================================
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists == False:
            raise ValidationError({"message": "Email does not exist"})
        return super().validate(attrs)
