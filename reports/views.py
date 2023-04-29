from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DoctorReport, NurseReport
from .serializer import (DoctorReportAllNursesSerializer, ResultNurseReportAddedDoctorSerializer,
                         ResultDoctorReportAddedNurseSerializer, NurseReportAllDoctorsSerializer,
                         DoctorReportSerializer, ResultDoctorReportSerializer, NurseReportSerializer, ResultNurseReportSerializer)
from rest_framework.permissions import IsAuthenticated
from users.models import (Nurse, Patient, Doctor, User)
from users.permissions import IsDoctor, IsNurse
from django.db.models import Prefetch
from project.notify_global import send_notification
from django.shortcuts import get_object_or_404
from fcm_django.models import FCMDevice
from project.serializer_error import serializer_error


# ======================= Doctor =======================================
class AddDoctorReport(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = ResultDoctorReportSerializer

    def post(self, serializer):
        data = self.request.data
        patient = get_object_or_404(Patient, id=data.get('patient'))
        nurse_ids = data.get('nurse')
        nurse_devices = {}
        for nurse_id in nurse_ids:
            nurse = User.objects.get(id=nurse_id)
            devices = FCMDevice.objects.filter(user=nurse)
            for device in devices:
                nurse_devices[device.registration_id] = nurse
        doctor = Doctor.objects.select_related(
            'user').get(user=self.request.user)
        serializer = DoctorReportSerializer(data=data)
        if serializer.is_valid():
            for device_token, nurse in nurse_devices.items():
                send_notification(patient, nurse, device_token,
                                  'Report Added', self.request.user)
            serializer.save(added_by=doctor)
            return Response(data={"message": "Report Created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)

    def get(self, request):
        doctor = Doctor.objects.select_related('user').get(user=request.user)
        reports = doctor.doctor_reports.all().prefetch_related(
            Prefetch('nurse', queryset=Nurse.objects.select_related('user'))
        )
        serializer = self.serializer_class(reports, many=True)
        return Response({"result": reports.count(), 'data': serializer.data})


class DoctorDetailsReport(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = ResultDoctorReportSerializer

    def get(self, request, id=None):
        report = get_object_or_404(DoctorReport.objects.select_related(
            'added_by', 'patient').prefetch_related('nurse'), id=id)
        serializer = self.serializer_class(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id=None):
        report = get_object_or_404(DoctorReport.objects.select_related(
            'added_by', 'patient').prefetch_related('nurse'), id=id)
        doctor = Doctor.objects.get(user=self.request.user)
        data = request.data
        serializer = DoctorReportSerializer(instance=report, data=data)

        if serializer.is_valid():
            result = serializer.save(added_by=doctor)
            response = {
                "message": "Report Updated successfully",
                "data": ResultDoctorReportSerializer(result).data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return serializer_error(serializer)

    def delete(self, request, id=None):
        report = get_object_or_404(DoctorReport.objects.select_related(
            'added_by', 'patient').prefetch_related('nurse'), id=id)
        report.delete()
        return Response({"message": "Report Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Return Report For Doctor (That Nurse added for him)
class GetDoctorReport(views.APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, id=None):
        user = request.user
        if id:
            report = NurseReport.objects.get(id=id)
            serializer = ResultDoctorReportAddedNurseSerializer(report)
            return Response({"report": serializer.data}, status=status.HTTP_200_OK)

        else:
            current_doctor = get_object_or_404(
                Doctor.objects.select_related('user'), user_id=user)
            report = current_doctor.doctors_reports.all().prefetch_related(
                Prefetch('nurse', queryset=Nurse.objects.select_related('user')))

            serializer = ResultDoctorReportAddedNurseSerializer(
                report, many=True)
            return Response({'result': len(serializer.data), "data": serializer.data}, status=status.HTTP_200_OK)


# ======================= Nurse =======================================
class AddNurseReport(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsNurse]
    serializer_class = ResultNurseReportSerializer

    def post(self, serializer):
        data = self.request.data
        patient = get_object_or_404(Patient, id=data.get('patient'))
        doctor_ids = data.get('doctor')
        doctor_devices = {}
        for doctor_id in doctor_ids:
            doctor = User.objects.get(id=doctor_id)
            devices = FCMDevice.objects.filter(user=doctor)
            for device in devices:
                doctor_devices[device.registration_id] = doctor
        nurse = Nurse.objects.select_related(
            'user').get(user=self.request.user)
        serializer = NurseReportSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            for device_token, doctor in doctor_devices.items():
                send_notification(
                    patient, doctor, device_token, 'Report Added', self.request.user)
            # serializer.save(added_by=nurse)
            return Response(data={"message": "Report Created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)

    def get(self, request):
        current_nurse = Nurse.objects.select_related(
            'user').get(user=request.user)
        report = current_nurse.nurses_reports.all().prefetch_related(
            Prefetch('doctor', queryset=Doctor.objects.select_related('user'))
        )
        serializer = self.serializer_class(report, many=True)

        return Response({"result": report.count(), 'data': serializer.data})


class NurseDetailsReport(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsNurse]
    serializer_class = ResultNurseReportSerializer

    def get(self, request, id=None):
        report = get_object_or_404(NurseReport.objects.select_related(
            'added_by', 'patient').prefetch_related('doctor'), id=id)
        serializer = self.serializer_class(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id=None):
        report = get_object_or_404(NurseReport.objects.select_related(
            'added_by', 'patient').prefetch_related('doctor'), id=id)
        nurse = Nurse.objects.get(user=self.request.user)
        data = request.data
        serializer = NurseReportSerializer(instance=report, data=data)

        serializer.is_valid(raise_exception=True)
        result = serializer.save(added_by=nurse)
        response = {
            "message": "Report Updated successfully",
            "data": self.serializer_class(result).data,
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        report = get_object_or_404(NurseReport.objects.select_related(
            'added_by', 'patient').prefetch_related('doctor'), id=id)
        report.delete()
        return Response({"message": "Report Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Return Report For Nurse (That Doctor added for her)
class GetNurseReport(views.APIView):
    permission_classes = [IsAuthenticated, IsNurse]

    def get(self, request, id=None):
        user = request.user
        if id:
            report = get_object_or_404(DoctorReport.objects.select_related(
                'patient', 'added_by').prefetch_related('nurse'), id=id)
            serializer = ResultNurseReportAddedDoctorSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            current_nurse = Nurse.objects.select_related(
                'user').get(user_id=user)
            report = current_nurse.nurse_reports.select_related(
                'patient', 'added_by').all()
            serializer = ResultNurseReportAddedDoctorSerializer(
                report, many=True)
            return Response({'result': len(serializer.data), "data": serializer.data}, status=status.HTTP_200_OK)


# ======================= Return & Add Report For patient =======================================
class DoctorPatientReport(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        reports = patient.patient_reports.prefetch_related('nurse__user').all()
        serializer = ResultDoctorReportSerializer(reports, many=True)
        return Response({'result': len(serializer.data), "data": serializer.data}, status=status.HTTP_200_OK)


class DoctorPatientReportDetail(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, id=None):
        report = get_object_or_404(
            DoctorReport.objects.prefetch_related("nurse__user"), id=id)
        serializer = ResultDoctorReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NursePatientReport(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        reports = patient.patients_reports.prefetch_related(
            'doctor__user').all()
        serializer = ResultNurseReportSerializer(reports, many=True)
        return Response({'result': len(serializer.data), "data": serializer.data}, status=status.HTTP_200_OK)


class NursePatientReportDetail(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, id=None):
        report = report = get_object_or_404(
            NurseReport.objects.prefetch_related("doctor__user"), id=id)
        serializer = ResultNurseReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ========== AddDoctorReportForAllNurse ===========
class AddDoctorReportForAllNurse(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorReportAllNursesSerializer

    def post(self, serializer, pk=None):
        data = self.request.data
        doctor = Doctor.objects.select_related(
            'user').get(user=self.request.user)
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
                send_notification(
                    patient, nurse_id, device_token, 'Report Added', self.request.user)

            serializer.save(added_by=doctor, nurse=nurses)
            return Response(data={"message": "Report Created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)


# ========== AddNurseReportForAllDoctors ===========
class AddNurseReportForAllDoctors(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NurseReportAllDoctorsSerializer

    def post(self, serializer, pk=None):
        data = self.request.data
        nurse = Nurse.objects.select_related(
            'user').get(user=self.request.user)
        patient = get_object_or_404(Patient, id=data.get('patient'))
        doctors = patient.doctor.all()
        doctor_devices = {}
        for doctor_id in doctors:
            devices = FCMDevice.objects.filter(user=doctor_id.user)
            for device in devices:
                doctor_devices[device.registration_id] = doctor_id.user
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            for device_token, doctor in doctor_devices.items():
                print(device_token)
                send_notification(
                    patient, doctor, device_token, 'Report Added', self.request.user)
            serializer.save(added_by=nurse, doctor=doctors)
            return Response(data={"message": "Report Created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)
