from rest_framework import generics, status
from fcm_django.models import FCMDevice
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .email_send import send_via_email, send_otp_via_email
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .permissions import IsAdminRole, IsNurse, IsDoctor, IsSuperUser
from .serializer import (SignUpAdminSerializer, SignUpUserSerializer, AddNurseSerializer, UpdateUserSerializer,
                         UserSerializer, SimpleUserSerializer, NurseSerializer, DoctorSerializer, UsersName,
                         AddPatient, PatientSerializer, PatientDoctorsSerializer, PatientNurseSerializer,
                         ResetPasswordSerializer, VerifyOtpSerializer, PasswordSerializer, UpdateProfileSerializer)
from .models import (Admin, Doctor, Nurse, User, Patient)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model
User = get_user_model()


# ---------- SignUp Admin View
class SignUpAdminView(generics.GenericAPIView):
    serializer_class = SignUpAdminSerializer

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            Token.objects.create(user=user).key
            response = {
                "message": "User Created Successfully , wait for accept",
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)


# ---- GetPendingAdminUser-------
class GetPendingAdminUser(generics.ListCreateAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = SimpleUserSerializer

    def get(self, request):
        queryset = User.objects.filter(is_active=False)
        serializer = self.serializer_class(queryset, many=True).data
        return Response(data={"result": len(serializer), "data": serializer}, status=status.HTTP_200_OK)


# ---- Get Pending Details AdminUser -------
class DetailsAdminUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SimpleUserSerializer
    queryset = User.objects.all()


class UpdateProfileAdmin(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request):
        user = request.user
        data = request.data
        phone_exists = User.objects.exclude(
            pk=user.pk).filter(phone=data["phone"]).exists()
        email_exists = User.objects.exclude(
            pk=user.pk).filter(email=data["email"]).exists()

        if phone_exists:
            return Response({"message": "Phone has already been used"}, status=status.HTTP_400_BAD_REQUEST)
        if email_exists:
            return Response({"message": "Email has already been used"}, status=status.HTTP_400_BAD_REQUEST)

        user.email = data.get('email')
        user.name = data.get('name')
        user.phone = data.get('phone')
        user.save()
        return Response({"message": "Update profile"}, status=status.HTTP_200_OK)


# ---- Get Pending Details AdminUser -------
class AccepterAdminUser(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        send_via_email(email)
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return Response({"message": 'Accept User'}, status=status.HTTP_200_OK)


# ---- GetActiveAdminUser -------
class GetActiveAdminUser(generics.ListCreateAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = SimpleUserSerializer

    def get(self, request):
        queryset = User.objects.filter(is_active=True, role='admin')
        serializer = self.serializer_class(queryset, many=True).data
        return Response(data={"result": len(serializer), "data": serializer}, status=status.HTTP_200_OK)


# ---------- SignUp View
class SignUpUserView(generics.CreateAPIView):
    permission_classes = [IsAdminUser, IsAdminRole]
    serializer_class = SignUpUserSerializer

    def post(self, request: Request):
        data = request.data
        user_added = request.user

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(added_by=user_added)
            response = {
                "message": "User Created Successfully",
                "status": 201
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)


# ---------- Login View
class Login(ObtainAuthToken):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        email = User.objects.filter(email=data.get('username'))

        if email.exists() and email.get().is_active == True:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            # Retrieve device token from request data
            device_token = request.data.get("device_token")
            FCMDevice.objects.get_or_create(
                registration_id=device_token, user=user)
            token, create = Token.objects.get_or_create(user=user)
            response = {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                'token': token.key,
                "message": "Login Success",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Email or Password is invalid"}, status=status.HTTP_400_BAD_REQUEST)


# ----- Logout
class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


# -------- Get Login User (Profile)
class LoginUser(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user_id = request.user.id
        queryset = User.objects.get(id=user_id)
        user_serializer = self.serializer_class(queryset)
        if user_serializer:
            return Response({"data": user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": user_serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----- Add or Remove Nurse from Doctor
class AddDeleteNurseUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminRole, IsAdminUser]
    serializer_class = AddNurseSerializer

    def post(self, request: Request):
        data = request.data
        doctor = data.get('doctor')
        nurses_ids = data.get('nurse')
        serializer = self.serializer_class(data=data)

        doctor_instance = Doctor.objects.get(user=doctor)
        if serializer.is_valid():
            for nurse_id in nurses_ids:
                nurse_instance = Nurse.objects.get(user_id=nurse_id)
                doctor_instance.nurse.add(nurse_instance)
                doctor_instance.save()
            return Response({"message": "Nurse Added successfully"}, status=status.HTTP_201_CREATED)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        data = request.data
        # Get Doctor
        doctor_instance = Doctor.objects.get(user=data['doctor'])
        # Get Nurse For Delete
        nurse_instance = Nurse.objects.get(user=data['nurse'])
        doctor_instance.nurse.remove(nurse_instance)
        return Response({"message": "Nurse deleted"}, status=status.HTTP_204_NO_CONTENT)


# ----- Return Nurses for doctor
class NurseDoctor(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = NurseSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Nurse.objects.prefetch_related('doctor_nurse')
        if pk := self.kwargs.get('pk'):
            queryset = queryset.select_related('user').filter(user_id=pk)
        else:
            doctor = get_object_or_404(Doctor.objects.prefetch_related(
                'nurse').select_related('user'), user_id=user.id)
            queryset = doctor.nurse.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = {"result": len(queryset), "data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)


# ----- Return Doctors for Nurse
class DoctorNurse(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsNurse]
    serializer_class = DoctorSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Doctor.objects.prefetch_related('doctor_nurse')
        if pk := self.kwargs.get('pk'):
            queryset = queryset.select_related('user').filter(user_id=pk)
        else:
            nurse = get_object_or_404(Nurse.objects.prefetch_related(
                'doctor_nurse').select_related('user'), user_id=user.id)
            queryset = nurse.doctor_nurse.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = {"result": len(queryset), "data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)


# -------- Get Doctors (Admin)
class AllDoctors(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = UserSerializer

    def get(self, request):
        user = self.request.user
        query = User.objects.select_related('added_by').filter(
            Q(added_by=user) & Q(role='doctor'))
        serializer = self.serializer_class(query, many=True).data
        return Response({"result": query.count(), 'data': serializer}, status=status.HTTP_200_OK)


# -------- Get Nurses (Admin)
class AllNurses(generics.ListCreateAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = self.request.user
        query = User.objects.select_related('added_by').filter(
            Q(added_by=user) & Q(role='nurse'))
        serializer = self.serializer_class(query, many=True).data
        return Response({"result": query.count(), 'data': serializer}, status=status.HTTP_200_OK)


# -------- Get Only Users (Updated Delete)
class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = UserSerializer
    queryset = User.objects.select_related('added_by').all()

    def get(self, request, pk=None):
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,  pk=None):
        user = self.get_object()
        data = request.data
        serializer = UpdateUserSerializer(instance=user, data=data)

        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        response = {
            "message": "User Updated successfully",
            "data": UserSerializer(result).data,
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response({"message": "User Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ----- Add Patients -----------
class SignupPatients(generics.CreateAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    serializer_class = AddPatient

    def post(self, request: Request):
        data = request.data
        user_added = request.user
        admin = Admin.objects.select_related('user').get(user_id=user_added.id)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(added_by=admin)
            response = {
                "message": "Patient Created Successfully",
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)


# ----- Patients for admin ---------
class Patients(generics.ListCreateAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    serializer_class = PatientSerializer

    def get(self, request):
        admin = Admin.objects.get(user_id=self.request.user)
        queryset = admin.added_admin.prefetch_related(
            'doctor__user', 'nurse__user')
        serializer = PatientSerializer(queryset, many=True).data
        return Response({"result": queryset.count(), 'data': serializer}, status=status.HTTP_200_OK)


# ----- Patient Details ---------
class PatientDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = Patient.objects.select_related(
        'added_by').prefetch_related('nurse', 'doctor')

    def get(self, request, pk=None):
        queryset = self.get_object()
        data = self.serializer_class(queryset).data
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        patient = self.get_object()
        data = request.data
        serializer = AddPatient(instance=patient, data=data)

        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        response = {
            "message": "Patient Updated successfully",
            "patient": self.serializer_class(result).data,
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        queryset = self.get_object()
        queryset.delete()
        return Response(data={"message": 'Patient Deleted'}, status=status.HTTP_200_OK)


# ----- Delete Doctor or Nurse from Patient
class PatientDeleteUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    serializer_class = AddPatient

    def delete(self, request, pk=None):
        data = request.data

        # Get patient
        patient_instance = Patient.objects.get(id=data['patient'])

        # Get User For Delete
        user = data['user']
        user_instance = User.objects.get(id=user)

        if user_instance.role == 'doctor':
            doctor = Doctor.objects.get(user=user_instance)
            patient_instance.doctor.remove(doctor)
            return Response({"message": "Doctor deleted"}, status=status.HTTP_204_NO_CONTENT)

        else:
            nurse = Nurse.objects.get(user=user_instance)
            patient_instance.nurse.remove(nurse)
            return Response({"message": "Nurse deleted"}, status=status.HTTP_204_NO_CONTENT)


# (Admin) Return Patient For one (nurse , or doctor)
class GetUsersPatient(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
        if user.role == 'doctor':
            doctor = Doctor.objects.get(user=user)
            patients = Patient.objects.filter(
                doctor=doctor).prefetch_related('nurse__user')
            serializer = PatientDoctorsSerializer(patients, many=True)
            return Response({"result": patients.count(), "data": serializer.data}, status=status.HTTP_200_OK)

        else:
            nurse = Nurse.objects.get(user=user)
            patients = Patient.objects.filter(
                nurse=nurse).prefetch_related('doctor__user')
            serializer = PatientNurseSerializer(patients, many=True)
            return Response({"result": patients.count(), "data": serializer.data}, status=status.HTTP_200_OK)


# ----- Return Patient for doctor and nurse
class PatientUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # --------------------------------
        if user.role == 'doctor' or user.role == 'Doctor':
            doctor = Doctor.objects.prefetch_related(
                'doctor').select_related('user').get(user_id=user.id)
            patients = doctor.doctor.all()
            serializer = PatientDoctorsSerializer(patients, many=True,)
            return Response({"result": patients.count(), "data": serializer.data}, status=status.HTTP_200_OK)

        # --------------------------------
        elif user.role == 'nurse' or user.role == 'Nurse':
            nurse = Nurse.objects.prefetch_related(
                'nurse').select_related('user').get(user_id=user.id)
            patients = nurse.nurse.all()
            serializer = PatientNurseSerializer(patients, many=True)

            return Response({"result": patients.count(), "data": serializer.data}, status=status.HTTP_200_OK)


class PatientUserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        queryset = Patient.objects.select_related(
            'added_by').prefetch_related('doctor', 'nurse').get(id=pk)

        if user.role == 'doctor':
            serializer = PatientDoctorsSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if user.role == 'nurse':
            serializer = PatientNurseSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetRelatedUser(APIView):
    permission_classes = [IsAdminRole, IsAuthenticated]

    def get(self, request, pk=None):
        user = get_object_or_404(
            User.objects.all(), id=pk)
        if user.role == 'doctor':
            doctor = get_object_or_404(Doctor, user__id=pk)
            nurses = doctor.nurse.all().select_related('user')
            serializer = NurseSerializer(nurses, many=True)
            count = nurses.count()

        elif user.role == 'nurse':
            nurse = get_object_or_404(Nurse, user__id=pk)
            doctors = nurse.doctor_nurse.all().select_related('user')
            serializer = DoctorSerializer(doctors, many=True)
            count = doctors.count()

        return Response({"count": count, "data": serializer.data}, status=status.HTTP_200_OK)


class DoctorsName(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = UsersName

    def get(self, request):
        doctors = User.objects.filter(role='doctor')
        serializer = self.serializer_class(doctors, many=True).data
        return Response(data={"data": serializer}, status=status.HTTP_200_OK)


class NursesName(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = UsersName

    def get(self, request):
        nurses = User.objects.filter(role='nurse')
        serializer = self.serializer_class(nurses, many=True).data
        return Response(data={"data": serializer}, status=status.HTTP_200_OK)


# ============================================================================
# Reset Password
# ============================================================================
class PasswordResetView(APIView):

    def post(self, request):
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            if not User.objects.filter(email=email).exists():
                return Response({"message": 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                send_otp_via_email(email)
                return Response({"message": 'code sent'}, status=status.HTTP_200_OK)
        else:
            return Response({"message": 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):

    def post(self, request):
        data = request.data
        serializer = VerifyOtpSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            otp = serializer.data['otp']

            user = User.objects.filter(email=email)

            if not user.exists():
                return Response({"message": 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp != otp:
                return Response({"message": 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp == otp:
                return Response({"message": "code done", "code": otp}, status=status.HTTP_200_OK)
        else:
            return Response({"message": 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordView(APIView):
    def post(self, request):
        data = request.data

        serializer = PasswordSerializer(data=data)
        if serializer.is_valid():
            password = serializer.data['password']
            email = serializer.data['email']
            user = User.objects.get(email=email)

            user.password = make_password(password)
            user.save()

            return Response({"message": "Password Reset Successfully"}, status=status.HTTP_201_CREATED)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
