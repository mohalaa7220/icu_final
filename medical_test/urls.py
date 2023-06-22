
from django.urls import path
from .views import ImageUploadView, AddDoctorMedical, PatientMedical, DetailsMedical, AddPatientMedicalImage, AddPatientRaysImage

urlpatterns = [
    path('', AddDoctorMedical.as_view(), name='doctor_medical'),
    path('<int:pk>', DetailsMedical.as_view(), name='DetailsMedical'),
    path('patient_medical/<str:pk>',
         PatientMedical.as_view(), name='patient_medical'),
    path('patient/<str:pk>/medical_image',
         AddPatientMedicalImage.as_view(), name='AddPatientMedicalImage'),
    path('patient/<str:pk>/rays_image',
         AddPatientRaysImage.as_view(), name='AddPatientRaysImage'),

    path('multi_images/', ImageUploadView.as_view(), name='image-create'),
]
