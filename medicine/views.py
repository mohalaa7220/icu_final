from rest_framework.response import Response
from rest_framework import generics, status, views
from .models import Medicines, Medicine
from rest_framework.permissions import IsAuthenticated
from .serializer import (MedicinesSerializer, AddMedicineSerializer, NurseResultMedicineSerializer,
                         AddAllNursesMedicineSerializer, ResultMedicineSerializer, SimpleResultMedicineSerializer)
from users.models import Nurse, Patient, User
from users.permissions import IsDoctor, IsNurse
from django.shortcuts import get_object_or_404
from project.notify_global import send_notification
from fcm_django.models import FCMDevice
from project.serializer_error import serializer_error
from datetime import datetime
from django.db.models import Q, F


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
class AddMedicineNurse(views.APIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = AddMedicineSerializer

    def post(self, request):
        data = request.data
        patient = get_object_or_404(Patient, id=data.get('patient'))
        nurse_ids = data.get('nurse')
        nurse_devices = {}
        for nurse_id in nurse_ids:
            nurse = User.objects.get(id=nurse_id)
            devices = FCMDevice.objects.filter(user=nurse)
            for device in devices:
                nurse_devices[device.registration_id] = nurse
        doctor_added = request.user
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save(doctor=doctor_added)
            for device_token, nurse in nurse_devices.items():
                send_notification(
                    patient, nurse, device_token, 'Medicine Added', self.request.user)
            return Response(data={"message": "Medicine saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)


# ------- Get Medicine for Doctor
class GetMedicineUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResultMedicineSerializer

    def get(self, request, pk=None):
        doctor = request.user
        if pk:
            medicine = Medicine.objects.select_related(
                'doctor', 'name', 'patient').prefetch_related("nurse").get(id=pk)
            serializer = self.serializer_class(medicine)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            selected_date = request.query_params.get('selected_date', None)
            if selected_date:
                selected_date_obj = datetime.strptime(
                    selected_date, '%Y-%m-%d').date()
                medicine = Medicine.objects.select_related('doctor', 'name', 'patient').prefetch_related(
                    "nurse").filter(Q(doctor=doctor) & Q(start_date=selected_date_obj))
            else:
                medicine = Medicine.objects.select_related('doctor', 'name', 'patient').prefetch_related(
                    "nurse").filter(doctor=doctor)
            serializer = self.serializer_class(medicine, many=True)
            return Response({"results": medicine.count(), "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        medicine = Medicine.objects.select_related(
            'doctor', 'name', 'patient').prefetch_related("nurse").get(id=pk)
        medicine.delete()
        return Response({"message": 'Medicine Delete Successfully'}, status=status.HTTP_200_OK)


# -------  Get Medicines for (Nurse)
class GetMedicineNurse(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsNurse]

    def get(self, request):
        user = request.user
        nurse = get_object_or_404(
            Nurse.objects.select_related('user'), user_id=user.id)
        selected_date = request.query_params.get('selected_date', None)
        if selected_date:
            selected_date_obj = datetime.strptime(
                selected_date, '%Y-%m-%d').date()
            medicine = Medicine.objects.select_related(
                'name', 'doctor', 'patient').filter(Q(nurse=nurse) & Q(start_date=selected_date_obj))
        else:
            medicine = Medicine.objects.select_related(
                'name', 'doctor', 'patient').filter(nurse=nurse)
        serializer = NurseResultMedicineSerializer(medicine, many=True)
        return Response({"results": medicine.count(), "data": serializer.data}, status=status.HTTP_200_OK)


# -------  Add Medicines for all Nurses
class AddMedicineAllNurses(views.APIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = AddAllNursesMedicineSerializer

    def post(self, request):
        data = request.data
        doctor_added = request.user
        patient = get_object_or_404(Patient, id=data.get('patient'))
        nurses = patient.nurse.all()
        nurse_devices = {}
        for nurse_id in nurses:
            devices = FCMDevice.objects.filter(user=nurse_id.user)
            for device in devices:
                nurse_devices[device.registration_id] = nurse_id.user
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            for device_token, nurse_id in nurse_devices.items():
                print(nurse_id)
                send_notification(
                    patient, nurse_id, device_token, 'Medicines Added', self.request.user)
            serializer.save(doctor=doctor_added, nurse=nurses)
            return Response(data={"message": "Medicine Added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)


# GetPatientDoctorMedicines
class GetPatientDoctorMedicines(views.APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, pk=None):
        doctor = request.user
        patient = get_object_or_404(Patient, id=pk)
        selected_date = request.query_params.get('selected_date', None)
        if selected_date:
            selected_date_obj = datetime.strptime(
                selected_date, '%Y-%m-%d').date()
            doctor_medicine = patient.patient_medicine.select_related('doctor', 'name').prefetch_related(
                "nurse__user").filter(Q(doctor=doctor) & Q(start_date=selected_date_obj))
        else:
            doctor_medicine = patient.patient_medicine.select_related('doctor', 'name').prefetch_related(
                "nurse__user").filter(doctor=doctor)
        serializer_class = ResultMedicineSerializer(
            doctor_medicine, many=True).data
        return Response({'result': doctor_medicine.count(), 'data': serializer_class}, status=status.HTTP_200_OK)


# GetPatientNurseMedicines
class GetPatientNurseMedicines(views.APIView):
    permission_classes = [IsAuthenticated, IsNurse]

    def get(self, request, pk=None):
        user = request.user
        nurse = get_object_or_404(
            Nurse.objects.select_related('user'), user_id=user.id)
        patient = get_object_or_404(Patient, id=pk)
        selected_date = request.query_params.get('selected_date', None)
        if selected_date:
            selected_date_obj = datetime.strptime(
                selected_date, '%Y-%m-%d').date()
            nurse_medicine = patient.patient_medicine.select_related('doctor', 'name').prefetch_related(
                "nurse__user").filter(Q(nurse=nurse) & Q(start_date=selected_date_obj))
        else:
            nurse_medicine = patient.patient_medicine.select_related('doctor', 'name').prefetch_related(
                "nurse__user").filter(nurse=nurse)
        serializer_class = NurseResultMedicineSerializer(
            nurse_medicine, many=True).data
        return Response({'result': nurse_medicine.count(), 'data': serializer_class}, status=status.HTTP_200_OK)


class CheckMedicine(views.APIView):
    def put(self, request):
        medicine_id = request.data.get('medicine_id')
        Medicine.objects.filter(id=medicine_id).update(
            status=True, updated=F('updated'))
        doctor = Medicine.objects.get(id=medicine_id).doctor
        patient = Medicine.objects.get(id=medicine_id).patient
        doctor_devices = {}
        devices = FCMDevice.objects.filter(user=doctor)
        for device in devices:
            doctor_devices[device.registration_id] = doctor
        for device_token, doctor in doctor_devices.items():
            send_notification(
                patient, doctor, device_token, 'Medicine Take', self.request.user)
        return Response({'message': "Done"}, status=status.HTTP_200_OK)
