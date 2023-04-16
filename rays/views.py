from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from .models import Rays, Doctor, Nurse, Patient
from .serializer import (DoctorRaysSerializer, ResultDoctorRaysSerializer)
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.permissions import IsDoctor, IsNurse


# ====================== Doctor =======================================
class AddDoctorRays(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = ResultDoctorRaysSerializer

    def post(self, serializer):
        data = self.request.data
        doctor = Doctor.objects.get(user=self.request.user)
        serializer = DoctorRaysSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(doctor=doctor)
            response = {
                "message": "Rays Added successfully",
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def get(self, request):
        user = request.user
        current_doctor = Doctor.objects.select_related('user').get(user=user)
        report = current_doctor.doctor_rays.select_related(
            'patient').prefetch_related('nurse')

        serializer = self.serializer_class(report, many=True)

        return Response({"result": report.count(), 'data': serializer.data})


# ====================== Nurse =======================================
class PatientRays(generics.ListCreateAPIView):
    def get(self, request, pk=None):
        patient = Patient.objects.get(pk=pk)
        rays = patient.patient_rays.all()
        print(rays)
        return Response({''}, status=status.HTTP_200_OK)
