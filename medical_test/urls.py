
from django.urls import path
from .views import AddDoctorMedical, PatientMedical, DetailsMedical

urlpatterns = [
    path('', AddDoctorMedical.as_view(), name='doctor_medical'),
    path('<int:pk>', DetailsMedical.as_view(), name='DetailsMedical'),
    path('patient_rays/<str:pk>', PatientMedical.as_view(), name='patient_medical'),
]
