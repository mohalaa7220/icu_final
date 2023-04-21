from django.urls import path
from .views import (AllNotifications, NotificationDetailView,
                    NotReadNotifications, CheckNotifications)

urlpatterns = [
    path('', AllNotifications.as_view(), name='notifications'),
    path('<int:pk>', NotificationDetailView.as_view(), name='notification'),
    path('unread_notification',
         NotReadNotifications.as_view(), name='notifications'),
    path('check_notification', CheckNotifications.as_view(), name='notifications'),
]
