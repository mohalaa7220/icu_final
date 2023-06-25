from rest_framework.response import Response
from rest_framework import status, views, generics
from rest_framework.permissions import IsAuthenticated
from .serializer import NotificationSerializer, NotificationHeadNursingSerializer
from .models import NotificationApp, Patient
from users.serializer import PatientSerializer
from django.db.models import Q


# AllNotifications
class AllNotifications(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = NotificationApp.objects.select_related(
            'user_sender', 'patient').filter(Q(user_receiver=request.user))
        serializer_class = NotificationSerializer(queryset, many=True).data
        return Response({'result': queryset.count(), "data": serializer_class}, status=status.HTTP_200_OK)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    queryset = NotificationApp.objects.select_related('user_sender', 'patient')


# ReadNotifications
class NotReadNotifications(views.APIView):
    serializer_class = NotificationSerializer

    def get(self, request):
        notification = NotificationApp.objects.select_related(
            'user_sender', 'patient').filter(status=False)
        serializer = self.serializer_class(notification, many=True).data
        return Response(data={"data": serializer}, status=status.HTTP_200_OK)


# Make ReadNotifications
class CheckNotifications(views.APIView):
    def put(self, request):
        data = request.data
        notification = NotificationApp.objects.select_related(
            'user_sender', 'patient').get(
            id=data.get('notification_id'))
        notification.status = True
        notification.save()
        return Response(data={'message': "Read done"}, status=status.HTTP_200_OK)


class AllNotificationPatient(views.APIView):
    def get(self, request, pk=None):
        patient = Patient.objects.get(id=pk)
        patient_notification = patient.patient_notification.all()
        serializer = NotificationSerializer(
            patient_notification, many=True).data
        return Response(data={'data': serializer}, status=status.HTTP_200_OK)


# Head Nursing

class NotificationHeadNursing(views.APIView):
    def get(self, request):
        notification = NotificationApp.objects.select_related(
            'user_sender', 'patient').prefetch_related('user_receiver').all()
        serializer = NotificationHeadNursingSerializer(
            notification, many=True).data
        return Response({'result': notification.count(), "data": serializer}, status=status.HTTP_200_OK)
