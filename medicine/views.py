from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Medicines, Medicine
from rest_framework.permissions import IsAuthenticated
from .serializer import (MedicinesSerializer, AddMedicineSerializer, NurseResultMedicineSerializer,
                         AddAllNursesMedicineSerializer, ResultMedicineSerializer, SimpleResultMedicineSerializer)
from users.models import Nurse, Patient
from users.permissions import IsDoctor
from django.shortcuts import get_object_or_404


# ------- Name of Medicines
class MedicinesView(generics.ListCreateAPIView):
    serializer_class = MedicinesSerializer

    def get(self, request):
        queryset = Medicines.objects.all()
        serializer = self.serializer_class(queryset, many=True).data
        return Response({"result": len(serializer), "data": serializer}, status=status.HTTP_200_OK)


# ------- Details Medicines
class MedicineDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicines.objects.all()
    serializer_class = MedicinesSerializer


# -------  Add Medicine for(patient)
class AddMedicineNurse(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = AddMedicineSerializer

    def post(self, request):
        data = request.data
        doctor_added = request.user
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save(doctor=doctor_added)
            response = {
                "message": "Medicine saved successfully",
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


# ------- Get Medicine for Doctor
class GetMedicineUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SimpleResultMedicineSerializer

    def get(self, request, pk=None):
        doctor = request.user
        if pk:
            medicine = Medicine.objects.select_related(
                'doctor', 'name', 'patient').prefetch_related("nurse").get(id=pk)
            serializer = self.serializer_class(medicine)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            medicine = Medicine.objects.select_related(
                'doctor', 'name', 'patient').prefetch_related("nurse").filter(doctor=doctor)
            serializer = ResultMedicineSerializer(medicine, many=True)
            return Response({"results": medicine.count(), "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        medicine = Medicine.objects.select_related(
            'doctor', 'name', 'patient').prefetch_related("nurse").get(id=pk)
        medicine.delete()
        return Response({"message": 'Medicine Delete Successfully'}, status=status.HTTP_200_OK)


# -------  Get Medicines for (Nurse)
class GetMedicineNurse(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        nurse = Nurse.objects.get(user_id=user.id)
        medicine = Medicine.objects.filter(nurse=nurse)
        serializer = NurseResultMedicineSerializer(medicine, many=True)
        return Response({"medicines": serializer.data}, status=status.HTTP_200_OK)


# -------  Add Medicines for all Nurses
class AddMedicineAllNurses(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddAllNursesMedicineSerializer

    def post(self, request):
        data = request.data
        doctor_added = request.user
        patient = Patient.objects.get(id=data.get('patient'))
        nurses = patient.nurse.all()
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            medicine = serializer.save(doctor=doctor_added, nurse=nurses)
            response = {
                "medicine": ResultMedicineSerializer(medicine, context=self.get_serializer_context()).data,
                "message": "Medicine saved successfully",
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
