from django.contrib import admin
from .models import MedicalTest, PatientMedicalImage, PatientRaysImage, Image
# Register your models here.


admin.site.register(MedicalTest)
admin.site.register(PatientMedicalImage)
admin.site.register(PatientRaysImage)
admin.site.register(Image)
