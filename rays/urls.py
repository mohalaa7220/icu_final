
from django.urls import path
from .views import AddDoctorRays, PatientRays, DetailsRays

urlpatterns = [
    path('', AddDoctorRays.as_view(), name='get_rays'),
    path('<int:pk>', DetailsRays.as_view(), name='get_rays'),
    path('patient_rays/<str:pk>', PatientRays.as_view(), name='patient_rays'),
]
