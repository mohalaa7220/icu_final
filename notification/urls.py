from django.urls import path
from .views import (AllNotifications, ReadNotifications, CheckNotifications)

urlpatterns = [
    path('', AllNotifications.as_view(), name='notifications'),
    path('read_notification',
         ReadNotifications.as_view(), name='notifications'),
    path('check_notification', CheckNotifications.as_view(), name='notifications'),
]
