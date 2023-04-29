from django.urls import path
from .views import (AllNotifications, NotificationDetailView, NotificationHeadNursing,
                    NotReadNotifications, CheckNotifications, AllNotificationPatient, AllPatients, PatientDetails)

urlpatterns = [
    path('', AllNotifications.as_view(), name='notifications'),
    path('<int:pk>', NotificationDetailView.as_view(), name='notification'),
    path('unread_notification',
         NotReadNotifications.as_view(), name='notifications'),
    path('check_notification', CheckNotifications.as_view(), name='notifications'),

    path('notifications_patient/<str:pk>', AllNotificationPatient.as_view(),
         name='notifications_patient'),

    path('notifications_head_nursing/', NotificationHeadNursing.as_view(),
         name='notifications_head_nursing'),
    path('all_patients/', AllPatients.as_view(), name='AllPatients'),
    path('all_patients/<str:pk>', PatientDetails.as_view(), name='PatientDetails'),
]
