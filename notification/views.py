from rest_framework.response import Response
from rest_framework import generics, status, views
from .serializer import NotificationSerializer
from .models import NotificationApp


# AllNotifications
class AllNotifications(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    queryset = NotificationApp.objects.select_related(
        'user_sender', 'patient').all()


# ReadNotifications
class ReadNotifications(views.APIView):
    serializer_class = NotificationSerializer

    def get(self, request):
        notification = NotificationApp.objects.select_related(
            'user_sender', 'patient').filter(status=False)
        serializer = self.serializer_class(notification, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)


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
