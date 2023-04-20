from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Patient, Rays
from .serializer import (
    DoctorRaysSerializer, ResultDoctorRaysSerializer, ResultPatientRaysSerializer)
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsDoctor
from django.shortcuts import get_object_or_404
from project.serializer_error import serializer_error
from project.notify_global import send_notification
from fcm_django.models import FCMDevice


# ====================== Doctor =======================================
class AddDoctorRays(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = ResultDoctorRaysSerializer

    def post(self, serializer):
        data = self.request.data
        doctor = get_object_or_404(
            Doctor.objects.select_related('user'), user=self.request.user)
        patient = get_object_or_404(Patient, id=data.get('patient'))
        nurses = patient.nurse.select_related('user').all()
        serializer = DoctorRaysSerializer(data=data)

        nurse_devices = {}
        for nurse_id in nurses:
            devices = FCMDevice.objects.filter(user=nurse_id.user)
            for device in devices:
                nurse_devices[device.registration_id] = nurse_id.user

        if serializer.is_valid():
            for device_token, nurse_id in nurse_devices.items():
                send_notification(
                    patient, nurse_id, device_token, 'Rays Added')
            serializer.save(doctor=doctor, nurse=nurses)
            return Response(data={"message": "Rays Added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)

    def get(self, request):
        user = request.user
        current_doctor = Doctor.objects.select_related('user').get(user=user)
        report = current_doctor.doctor_rays.select_related(
            'patient').prefetch_related('nurse__user')

        serializer = self.serializer_class(report, many=True)

        return Response({"result": report.count(), 'data': serializer.data})


class DetailsRays(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResultPatientRaysSerializer
    queryset = Rays.objects.select_related(
        'patient', 'doctor__user').prefetch_related('nurse__user').all()


# ====================== Nurse =======================================
class PatientRays(views.APIView):
    def get(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        rays = patient.patient_rays.prefetch_related(
            'nurse__user', 'doctor__user').all()
        serializer = ResultPatientRaysSerializer(rays, many=True).data
        return Response({'data': serializer}, status=status.HTTP_200_OK)
