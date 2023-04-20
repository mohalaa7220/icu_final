from django.contrib import admin
from .models import MedicalTest, PatientMedicalImage, PatientRaysImage
# Register your models here.


admin.site.register(MedicalTest)
admin.site.register(PatientMedicalImage)
admin.site.register(PatientRaysImage)
