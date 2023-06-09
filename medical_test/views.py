from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Patient, MedicalTest, Image
from .serializer import (DoctorMedicalSerializer, ResultDoctorMedicalSerializer, AddPatientMedicalImageSerializer,
                         ImageSerializer, AddImageSerializer, AddPatientRaysImageSerializer,
                         ResultPatientMedicalSerializer, PatientMedicalImageSerializer, PatientRaysImageSerializer)
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsDoctor
from users.models import User
from django.shortcuts import get_object_or_404
from project.serializer_error import serializer_error
from project.notify_global import send_notification, send_notification_headnursing
from fcm_django.models import FCMDevice
from datetime import datetime


# ====================== Doctor =======================================
class AddDoctorMedical(views.APIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = ResultDoctorMedicalSerializer

    def post(self, serializer):
        data = self.request.data
        doctor = get_object_or_404(
            Doctor.objects.select_related('user'), user=self.request.user)
        patient = get_object_or_404(Patient, id=data.get('patient'))
        nurses = patient.nurse.select_related('user').all()
        serializer = DoctorMedicalSerializer(data=data)

        nurse_devices = {}
        for nurse_id in nurses:
            devices = FCMDevice.objects.filter(user=nurse_id.user)
            for device in devices:
                nurse_devices[device.registration_id] = nurse_id.user

        if serializer.is_valid():
            if not bool(nurse_devices):
                print("The dictionary is empty.")
                send_notification_headnursing(
                    patient, 'Medical Test Added', self.request.user)
            else:
                print("The dictionary is not empty.")
                for device_token, nurse_id in nurse_devices.items():
                    send_notification(
                        patient, nurse_id, device_token, 'Medical Test Added', self.request.user)
            serializer.save(doctor=doctor, nurse=nurses)
            return Response(data={"message": "Medical Test Added"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)

    def get(self, request):
        user = request.user
        current_doctor = get_object_or_404(
            Doctor.objects.select_related('user'), user=user)
        medical = current_doctor.doctor_medical.select_related(
            'patient').prefetch_related('nurse__user')
        serializer = self.serializer_class(medical, many=True)
        return Response({"result": medical.count(), 'data': serializer.data})


class DetailsMedical(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResultPatientMedicalSerializer
    queryset = MedicalTest.objects.select_related(
        'patient', 'doctor__user').prefetch_related('nurse__user').all()


class PatientMedical(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        medical = patient.patient_medical.prefetch_related(
            'nurse__user', 'doctor__user').all()
        serializer = ResultPatientMedicalSerializer(medical, many=True).data
        return Response({'data': serializer}, status=status.HTTP_200_OK)


class AddPatientMedicalImage(generics.ListCreateAPIView):
    serializer_class = PatientMedicalImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=request.data.get('patient'))
        doctors = patient.doctor.select_related('user').all()
        images = request.data.get('images', [])
        if not images:
            return Response({"message": "at least add one image"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AddPatientMedicalImageSerializer(data=request.data)
        doctor_devices = {}
        for doctor_id in doctors:
            devices = FCMDevice.objects.filter(user=doctor_id.user)
            for device in devices:
                doctor_devices[device.registration_id] = doctor_id.user
        if serializer.is_valid():
            if not bool(doctor_devices):
                print("The dictionary is  empty.")
                send_notification_headnursing(
                    patient, 'Image  Medical Test Upload', self.request.user)
            else:
                print("The dictionary is not empty.")
                for device_token, doctor in doctor_devices.items():
                    send_notification(patient, doctor, device_token,
                                      'Image  Medical Test Upload', self.request.user)
            serializer.save()
            return Response({'message': 'Image  Medical Test added successfully'}, status=status.HTTP_200_OK)
        else:
            return serializer_error(serializer)

    def get(self, request, pk=None):
        print("self.request", self.request.user)
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        patient_medical_image = patient.patient_medical_image.all()
        serializer = self.serializer_class(
            patient_medical_image,
            many=True,
            context={'request': request}
        ).data
        return Response({'data': serializer}, status=status.HTTP_200_OK)


class AddPatientRaysImage(generics.ListCreateAPIView):
    serializer_class = PatientRaysImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        patient_id = request.data.get('patient')
        images = request.data.get('images', [])

        if not images:
            return Response({"message": "Please add at least one image"}, status=status.HTTP_400_BAD_REQUEST)

        patient = get_object_or_404(Patient, pk=patient_id)
        doctors = patient.doctor.select_related('user').all()

        serializer = AddPatientRaysImageSerializer(data=request.data)

        doctor_devices = {}
        for doctor in doctors:
            devices = FCMDevice.objects.filter(user=doctor.user)
            for device in devices:
                doctor_devices[device.registration_id] = doctor.user

        if serializer.is_valid():
            if not doctor_devices:
                print("The dictionary is empty.")
                send_notification_headnursing(
                    patient, 'Image Rays Upload', self.request.user)
            else:
                print("The dictionary is not empty.")
                for device_token, doctor in doctor_devices.items():
                    send_notification(
                        patient, doctor, device_token, 'Image Rays Upload', self.request.user)

            serializer.save()
            return Response({'message': 'Image Rays added successfully'}, status=status.HTTP_200_OK)
        else:
            return serializer_error(serializer)

    def get(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        patient_medical_image = patient.patient_rays_image.all()
        serializer = self.serializer_class(
            patient_medical_image, many=True, context={'request': request}).data
        return Response({'data': serializer}, status=status.HTTP_200_OK)


class ImageUploadView(generics.ListCreateAPIView):
    serializer_class = ImageSerializer

    def post(self, request):
        serializer = AddImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Upload Successfully"}, status=status.HTTP_200_OK)

    def get(self, request):
        selected_date = request.query_params.get('selected_date', None)
        if selected_date:
            selected_date_obj = datetime.strptime(
                selected_date, '%Y-%m-%d').date()
            queryset = Image.objects.filter(created__date=selected_date_obj)
        else:
            queryset = Image.objects.all()
        serializer = self.serializer_class(queryset, many=True).data
        return Response({'results': len(serializer), "data": serializer}, status=status.HTTP_200_OK)
